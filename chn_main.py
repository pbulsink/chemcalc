import os
import webapp2
import jinja2
import logging
import hmac
from ast import literal_eval
from script.parse import parse  # Import the parser
from script.solvent_correct import get_ea, solvent_calculate  # Import the calculator
from script.secret import secret  # Keep the secret from the open source files.
from script.elements_list import ELEMENTS

# from google.appengine.ext import db

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True)


def check_secure_val(secure_val):
    """Verify value is unmodified, and return it"""
    if secure_val == "":
        return ""
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val
    else:
        return None


def is_floatable(s):
    """
    Return true/false if string is float number
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def make_secure_val(val):
    """Write string with value, hash, for cookies security checking"""
    return '%s|%s' % (str(val), hmac.new(secret, str(val)).hexdigest())


def parse_formula(formula, error):
    """
    Parse formula to list of elements and number of appearances. Catch bad
    formulas and return error.
    """
    valid_formula = ""
    try:
        valid_formula = parse(formula).return_elements()
    except ValueError:
        valid_formula = None
        error = error + "Not a valid Formula"
    except:
        error = error + "Unknown Error. "
    return valid_formula, error


def render_results(results, exp, solvent, formula):
    """
    Turn results recieved from solvent_correct into those passable
    to the template
    """
    rendered_results = dict()
    eresult = results[1]
    rexp = list(list())
    ulexp = list(list())
    sresult = list(list())
    rendered_results['diff'] = ""
    rendered_results['result_formula'] = ""  # formula
    rendered_results['rtype'] = "ea"
    rendered_results['mmass'] = results[2]

    # C and H go first in list
    if "C" in eresult:
        if "C" in exp:
            expc = float(exp["C"])
        else:
            expc = 0.0
        rexp.append(["C", expc, eresult["C"]])
        del eresult["C"]
    if "H" in eresult:
        if "H" in exp:
            exph = float(exp["H"])
        else:
            exph = 0.0
        rexp.append(["H", exph, eresult["H"]])
        del eresult["H"]
    ulexp = eresult.items()
    if ulexp != []:
        for u in ulexp:
            if u[0] in exp:
                expu = float(exp[u[0]])
            else:
                expu = 0.0
            rexp.append([u[0], expu, u[1]])

    if results[0] != "ea":
        # Full calculation. Change rtype, process more.
        rendered_results['rtype'] = "calc"
        sresult = results[3]
        cresult = results[4]
        # Aligning with C and H
        if "C" in cresult:
            rexp[0].append(cresult["C"])
            del cresult["C"]
        if "H" in cresult:
            if rexp[1][0] == "H":
                rexp[1].append(cresult["H"])
            else:
                rexp[0].append(cresult["H"])
            del cresult["H"]
        cresult.items()
        for r in rexp:
            if r[0] in cresult:
                r.append(cresult[r[0]])
        for r in rexp:
            try:
                r.append(float(r[3] - float(r[1])))
            except:
                logging.exception("error ln 116 %s, %s" % (str(r[0]), str(rexp)))
        rendered_results['diff'] = results[5]
        # result_formula = formula + '*'
        # eventual printing out of formula * solvents.
        # requires dictionary or modified solvent_correct.
        # logging.info(str(sresult))
        # for s in sresult:
        #    result_formula = result_formula + ("%0.2f" % s[1]) + s[3]

    # Build rendered_results from components.
    rendered_results['exp'] = rexp
    rendered_results['solvent'] = sresult
    return rendered_results


class Handler(webapp2.RequestHandler):
    """Handler for webapp cuts repeats."""
    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))

    def render_str(self, template, **params):
        t = JINJA_ENV.get_template(template)
        return t.render(params)

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def handle_exception(self, exception, debug):
        """Handle html exceptions"""
        # Log the error.
        logging.exception(exception)

        # Set a custom message.
        self.response.write('An error occurred.')

        # If the exception is a HTTPException, use its error code.
        # Otherwise use a generic 500 error code.
        if isinstance(exception, webapp2.HTTPException):
            self.redirect('/ea/?r=%s' % exception)
        else:
            self.redirect('/ea/?r=e')


class AboutHandler(Handler):
    """Simple about-us handler"""
    def get(self):
        self.render("about.html")


class ContactHandler(Handler):
    """Simple Contact-Us handler"""
    def get(self):
        self.render("contact.html")


class EaResultHandler(Handler):
    """Requests calculation, rendering, draw results"""
    def get(self):
        solvent = list()
        exp = dict()
        formula = check_secure_val(self.request.cookies.get('f'))
        if not formula:
            self.redirect('/ea/?r=ecf')
        fparsed, e = parse_formula(formula, "")
        s = check_secure_val(self.request.cookies.get('s'))
        if s:
            solvent = literal_eval(s)
        elif s is None:
            self.redirect('/ea/r=ecs')
        e = check_secure_val(self.request.cookies.get('e'))
        if e:
            exp = dict(literal_eval(e))
        elif e is None:
            self.redirect('/ea/?r=ece')

        if formula == "":
            self.redirect('/ea/?r=nf')
        elif solvent == []:
            results = get_ea(fparsed)
        else:
            results = solvent_calculate(fparsed, solvent, exp)
        rendered_results = render_results(results, exp, solvent, formula)

        template_values = {'formula': formula,
                           'rtype': rendered_results['rtype'],
                           'exp': rendered_results['exp'],
                           'solvent': rendered_results['solvent'],
                           'diff': rendered_results['diff'],
                           'result_formula': rendered_results['result_formula'],
                           'mmass': rendered_results['mmass']}
        self.render('results.html', **template_values)


class EaHelpHandler(Handler):
    """Simple help handler"""
    def get(self):
        self.render("eahelp.html")


class EaMainPage(Handler):
    """Main page. Handles form POST, and flagged returns (errors, etc.)"""
    def render_front(self, template_values):
        """Draw the front page, filling fields if supplied"""
        self.render("eaform.html", **template_values)

    def get(self):
        """Prep the front page for rendering"""
        other_variables = [["", "other1"],
                           ["", "other2"],
                           ["", "other3"]]
        e_var = [["C", "exp_c", ""],
                 ["H", "exp_h", ""],
                 ["N", "exp_n", ""],
                 ["O", "exp_o", ""],
                 ["S", "exp_s", ""],
                 ["P", "exp_p", ""],
                 ["F", "exp_f", ""],
                 ["Cl", "exp_cl", ""],
                 ["Br", "exp_br", ""],
                 ["I", "exp_i", ""]]
        solvent_list = [["H2O", ["Water", False]],
                        ["CH2Cl2", ["Methylene Chloride", False]],
                        ["CHCl3", ["Chloroform", False]],
                        ["CH3COH", ["Acetone", False]],
                        ["CH3CN", ["Acetonitrile", False]],
                        ["C7H8", ["Toluene", False]],
                        ["CH3OH", ["Methanol", False]],
                        ["CH3COH3", ["Ethanol", False]],
                        ["C6H14", ["Hexanes", False]],
                        ["C6H6", ["Benzene", False]],
                        ["CH3CH3SO", ["DMSO", False]]]

        error = ""
        formula = ""
        #Handle returns of different types
        r = self.request.get('r')
        if r:
            if r == 'nf':
                error = "You need to enter information before getting results. "
            elif r == "r":
                for s in solvent_list:
                    s[1][1] = False
            elif r == "c":
                formula = check_secure_val(self.request.cookies.get('f'))
                s = check_secure_val(self.request.cookies.get('s'))
                if s:
                    sol = literal_eval(s)
                    for s in sol:
                        for t in solvent_list:
                            if s[0] == t[1][0]:
                                t[1][1] = True
                e = check_secure_val(self.request.cookies.get('e'))
                if e:
                    exp = literal_eval(e)
                    for e in exp:
                        for f in e_var:
                            if e[0] == f[0]:
                                f[2] = e[1]
            elif r == 'e':
                error = "Woops! Something went wrong. The admin has been notified. Please try again, refresh the page, or come back in a few days if it still doesn't work"
            elif r == 'ec':
                error = "Don't modify cookies... enter new values"
            elif r.isnumeric():
                error = "An error %s happened. Please try again" % r

        template_values = {"formula": formula, "exp_variables": e_var,
                           "solvent_variables": solvent_list, "error": error,
                           "other_variables": other_variables}
        self.response.set_cookie('f', "")
        self.response.set_cookie('s', "")
        self.response.set_cookie('e', "")
        self.render_front(template_values)

    def post(self):
        """Process the form"""
        error = ""
        o_var = [["", "other1"],
                 ["", "other2"],
                 ["", "other3"]]
        s_var = [["H2O", ["Water", False]],
                 ["CH2Cl2", ["Methylene Chloride", False]],
                 ["CHCl3", ["Chloroform", False]],
                 ["CH3COH", ["Acetone", False]],
                 ["CH3CN", ["Acetonitrile", False]],
                 ["C7H8", ["Toluene", False]],
                 ["CH3OH", ["Methanol", False]],
                 ["CH3COH3", ["Ethanol", False]],
                 ["C6H14", ["Hexanes", False]],
                 ["C6H6", ["Benzene", False]],
                 ["CH3CH3SO", ["DMSO", False]]]
        e_var = [["C", "exp_c", ""],
                 ["H", "exp_h", ""],
                 ["N", "exp_n", ""],
                 ["O", "exp_o", ""],
                 ["S", "exp_s", ""],
                 ["P", "exp_p", ""],
                 ["F", "exp_f", ""],
                 ["Cl", "exp_cl", ""],
                 ["Br", "exp_br", ""],
                 ["I", "exp_i", ""]]
        t_var = {"formula": "", "exp_variables": e_var,
                 "error": "", "solvent_variables": s_var,
                 "other_variables": o_var}
        solvents = []
        sget = self.request.get_all("solvent")
        for s in sget:
            name = ""
            for i in s_var:
                if str(s) == i[0]:
                    name = i[1][0]
                    i[1][1] = True
            solvents.append([name, str(s)])
        for o in o_var:
            d = str(self.request.get(o[1]))
            if d != "":
                valid, error = parse_formula(d, error)
                if valid:
                    solvents.append(["", d])
                    o[0] = d
        formula = self.request.get("formula")
        if not formula:
            error = error + "You need to enter a formula. "
        else:
            valid_formula, error = parse_formula(formula, error)

        exp = False
        for e in e_var:
            e[2] = str(self.request.get(e[1]))
            if not is_floatable(e[2]) and e[2] != "":
                error = error + "Not a number error for Experimental %s. " % e[0]
            elif e[2] != '':
                exp = True

        if exp is False:
            #want normal value
            if solvents == []:
                self.response.set_cookie('f', make_secure_val(formula))
                self.redirect("/ea/results/")
            else:
                #need to know how much solvent?
                error = error + "Can't calculate solvent inclusion without experimental values. To include co-crystallized solvents, use the * notation. "

        elif not error and solvents == "":
            #need some solvents to contaminate it!
            error = error + "Please select some solvents. "

        elif not error:
            experimentals = []
            for e in e_var:
                if e[2] != "":
                    experimentals.append((e[0], e[2]))
            self.response.set_cookie('f', make_secure_val(formula))
            self.response.set_cookie('s', make_secure_val(solvents))
            self.response.set_cookie('e', make_secure_val(experimentals))
            self.redirect("/ea/results/")

        if not error == "":
            for s in s_var:
                for t in solvents:
                    if t[1] == s[0]:
                        s[1][1] = True
            logging.info(solvents)
            t_var['formula'] = formula
            t_var['exp_var'] = e_var
            t_var['error'] = error
            t_var['solvent_variables'] = s_var
            t_var['other_variables'] = o_var
            self.render_front(t_var)


class HomeHandler(Handler):
    """Homepage"""
    def get(self):
        self.render("home.html")


class IsotopeHandler(Handler):
    """Prep and draw Isotope Page"""
    def render_page(self, template_values):
        """Draw the front page, filling fields if supplied"""
        self.render("mass_table.html", **template_values)

    def get(self):
        e = self.request.get('e')
        f = self.request.get('f')
        # Have to decide some way to handle mixed input. Do both!
        isotopes = list ()
        selected_elements = False
        if e in ELEMENTS:
            selected_elements = True
            if ELEMENTS[e].has_isotopes:
                for i in ELEMENTS[e].isotopes:
                    isotopes.append([ELEMENTS[e].name, ELEMENTS[e].sym,
                                     ELEMENTS[e].ano, i])
        if f in ELEMENTS:
            selected_elements = True
            if ELEMENTS[f].has_isotopes:
                for i in ELEMENTS[f].isotopes:
                    isotopes.append([ELEMENTS[f].name, ELEMENTS[f].sym,
                                     ELEMENTS[f].ano, i])
        if not selected_elements:
            elements = ELEMENTS
            for key in ELEMENTS:
                if ELEMENTS[key].has_isotopes:
                    for i in ELEMENTS[key].isotopes:
                        isotopes.append([ELEMENTS[key].name, ELEMENTS[key].sym,
                                         ELEMENTS[key].ano, i])
        
        element_symbols = list()
        element_names = list()
        for key in ELEMENTS:
            if ELEMENTS[key].has_isotopes:
                element_names.append([ELEMENTS[key].name, key])
                element_symbols.append([key, key])
        element_names.sort()
        element_symbols.sort()
        element_names.insert(0, ["All Elements", ""])
        element_symbols.insert(0, ["All Elements", ""])
        print isotopes
        isotopes = sorted(isotopes,
                          key=lambda isotopes: (isotopes[2], isotopes[3][0]))
        print "after"
        print isotopes
        template_values = {"elements": isotopes, "element_name": element_names,
                           "element_symbol": element_symbols}
        self.render_page(template_values)


class IsotopeHelpHandler(Handler):
    """Simple Isotope Help Handler"""
    def get(self):
        self.render("isotopehelp.html")


app = webapp2.WSGIApplication([('/ea/?', EaMainPage),
                               ('/ea/results/?', EaResultHandler),
                               ('/ea/help/?', EaHelpHandler),
                               ('/about/?', AboutHandler),
                               ('/contact/?', ContactHandler),
                               ('/isotopes/?', IsotopeHandler),
                               ('/isotopes/help/?', IsotopeHelpHandler),
                               ('/?', HomeHandler)
                               ], debug=True)

