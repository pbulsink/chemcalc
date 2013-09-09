import os
import webapp2
import urllib2
import jinja2
import logging
import hmac
from ast import literal_eval
from script.parse import * #Import the parser
from script.solvent_correct import * #Import the calculator
from script.secret import secret #Keep the secret from the open source files.

#from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

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
        y = float(s)
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
    Turn results recieved from solvent_correct into those passable to the template
    """
    rendered_results = dict()
    eresult = results[1]
    rexp=list(list())
    ulexp=list(list())
    sresult = list(list())
    diff = ""
    rendered_results['result_formula']=""#formula
    rtype="ea"
    rendered_results['mmass']=results[2]

    #C and H go first in list
    if eresult.has_key("C"):
        if exp.has_key("C"):
            expc=float(exp["C"])
        else:
            expc = 0.0
        rexp.append(["C", expc, eresult["C"]])
        del eresult["C"]
    if eresult.has_key("H"):
        if exp.has_key("H"):
            exph=float(exp["H"])
        else:
            exph = 0.0
        rexp.append(["H", exph, eresult["H"]])
        del eresult["H"]
    ulexp = eresult.items()
    if ulexp != []:
        for u in ulexp:
            if exp.has_key(u[0]):
                expu = float(exp[u[0]])
            else:
                expu = 0.0
            rexp.append([u[0], expu, u[1]])

    if results[0] != "ea":
        #Full calculation. Change rtype, process more.
        rtype="calc"
        sresult=results[3]
        cresult=results[4]
        #Aligning with C and H 
        if cresult.has_key("C"):
            rexp[0].append(cresult["C"])
            del cresult["C"]
        if cresult.has_key("H"):
            if rexp[1][0]=="H":
                rexp[1].append(cresult["H"])
            else:
                rexp[0].append(cresult["H"])
            del cresult["H"]
        cresult.items()
        for r in rexp:
            if cresult.has_key(r[0]):
                r.append(cresult[r[0]])
        for r in rexp:
            try:
                r.append(float(r[3]-float(r[1])))
            except:
                logging.exception("error ln 146 %s" % str(r))
        diff= results[5]
        result_formula = formula + '*'
        #eventual printing out of formula * solvents. requires dictionary or modified solvent_correct.
        #logging.info(str(sresult))
        #for s in sresult:
        #    result_formula = result_formula + ("%0.2f" % s[1]) + s[3]
    
    #Build rendered_results from components.
    rendered_results['rtype']=rtype
    rendered_results['exp']=rexp
    rendered_results['solvent']=sresult
    rendered_results['diff']=diff
    return rendered_results

#Handler to be inherited by everyone else. Handles errors better than generic 500.
class Handler(webapp2.RequestHandler):
    """Saves me from typing lots of repeat"""
    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def handle_exception(self, exception, debug):
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
        elif s == None:
            self.redirect('/ea/r=ecs')
        e = check_secure_val(self.request.cookies.get('e'))
        if e:
            exp = dict(literal_eval(e))
        elif e == None:
            self.redirect('/ea/?r=ece')
        sec_results = self.request.cookies.get('r')
        

        if sec_results == "" or sec_results == None:
            if formula == "":
                #No formula given. Arrives by typing in link?
                self.redirect('/ea/?r=nf')
            #Else new results needed
            elif solvent == []:
                results = get_ea(fparsed)
            else:
                results = solvent_calculate(fparsed, solvent, exp)
            rendered_results = render_results(results, exp, solvent, formula)
            self.response.set_cookie('r', make_secure_val(rendered_results))
        else:
            results = check_secure_val(sec_results)
            if not results:
                self.redirect('/ea/?r=ecr')
            rendered_results = literal_eval(results)

        template_values = {'formula':formula,
                           'rtype':rendered_results['rtype'],
                           'exp':rendered_results['exp'],
                           'solvent':rendered_results['solvent'],
                           'diff':rendered_results['diff'],
                           'result_formula':rendered_results['result_formula'],
                           'mmass':rendered_results['mmass']}
        self.render('results.html', **template_values)

class AboutHandler(Handler):
    """Simple about-us handler"""
    def get(self):
        self.render("about.html")

class EaHelpHandler(Handler):
    """Simple help handler"""
    def get(self):
        self.render("eahelp.html")

class ContactHandler(Handler):
    """Simple Contact-Us handler"""
    def get(self):
        self.render("contact.html")

class MainRedirectHandler(Handler):
    """Some link isn't fixed to /ea/. Post a log then redirect"""
    def get(self):
        r = self.request.get('r')
        sub = ""
        if r:
            sub = "/?r=%s" % r
        logging.error("Request to main /. With error: %s." % sub)
        self.redirect('/ea%s' % sub)

class EaMainPage(Handler):
    """Main page. Handles form POST, and flagged returns (errors, etc.)"""
    def render_front(self, template_values):
        """Draw the front page, filling fields if supplied"""
        self.render("submit-form.html", **template_values)
  
    def get(self):
        """Prep the front page for rendering"""
        other_variables = [["", "other1"],
                           ["", "other2"],
                           ["", "other3"]]
        e_var = [["C","exp_c", ""],
                 ["H","exp_h", ""],
                 ["N","exp_n", ""],
                 ["O","exp_o", ""],
                 ["S","exp_s", ""],
                 ["P","exp_p", ""],
                 ["F","exp_f", ""],
                 ["Cl","exp_cl", ""],
                 ["Br","exp_br", ""],
                 ["I","exp_i", ""]]
        solvent_list = [["H2O",["Water", False]],
                        ["CH2Cl2",["Methylene Chloride", False]],
                        ["CHCl3",["Chloroform", False]],
                        ["CH3COH",["Acetone", False]],
                        ["CH3CN",["Acetonitrile", False]],
                        ["C7H8",["Toluene", False]],
                        ["CH3OH",["Methanol", False]],
                        ["CH3COH3",["Ethanol", False]],
                        ["C6H14",["Hexanes", False]],
                        ["C6H6",["Benzene", False]],
                        ["CH3CH3SO",["DMSO", False]]]

        error = ""
        formula = ""
        #Handle returns of different types
        r = self.request.get('r')
        if r:
            if r == 'nf':
                error = "You need to enter information before getting results. "
            elif r == "r":
                for s in solvent_list:
                    s[1][1]=False
                self.response.set_cookie('f', "")
                self.response.set_cookie('s', "")
                self.response.set_cookie('e', "")
                self.response.set_cookie('r', "")
            elif r == "c":
                formula = check_secure_val(self.request.cookies.get('f'))
                self.response.set_cookie('r', "")
                s = check_secure_val(self.request.cookies.get('s'))
                if s:
                    sol = literal_eval(s)
                for s in sol:
                    for t in solvent_list:
                        if s[0]==t[1][0]:
                            t[1][1]=True
                e = check_secure_val(self.request.cookies.get('e'))
                if e:
                    exp = literal_eval(e)
                for e in exp:
                    for f in e_var:
                        if e[0] == f[0]:
                            f[2]=e[1]
            elif r == 'e':
                error = "Woops! Something went wrong. The admin has been notified. Please try again, refresh the page, or come back in a few days if it still doesn't work"
            elif r == 'ec':
                error = "Don't modify cookies... enter new values"
                self.response.set_cookie('f', "")
                self.response.set_cookie('s', "")
                self.response.set_cookie('e', "")
                self.response.set_cookie('r', "")
            elif r.isnumeric():
                error = "An error %s happened. Please try again" % r

        template_values = {"formula":formula, "exp_variables":e_var,
                           "solvent_variables":solvent_list, "error":error,
                           "other_variables":other_variables}
        self.render_front(template_values)

    def post(self):
        """Process the form"""
        error = ""
        o_var = [["", "other1"],
                 ["", "other2"],
                 ["", "other3"]]
        s_var = [["H2O",["Water", False]],
                 ["CH2Cl2",["Methylene Chloride", False]],
                 ["CHCl3",["Chloroform", False]],
                 ["CH3COH",["Acetone", False]],
                 ["CH3CN",["Acetonitrile", False]],
                 ["C7H8",["Toluene", False]],
                 ["CH3OH",["Methanol", False]],
                 ["CH3COH3",["Ethanol", False]],
                 ["C6H14",["Hexanes", False]],
                 ["C6H6",["Benzene", False]],
                 ["CH3CH3SO",["DMSO", False]]]
        e_var = [["C","exp_c", ""],
                 ["H","exp_h", ""],
                 ["N","exp_n", ""],
                 ["O","exp_o", ""],
                 ["S","exp_s", ""],
                 ["P","exp_p", ""],
                 ["F","exp_f", ""],
                 ["Cl","exp_cl", ""],
                 ["Br","exp_br", ""],
                 ["I","exp_i", ""]]
        t_var = {"formula":"", "exp_variables":e_var,
                 "error":"", "solvent_variables":s_var, "other_variables":o_var}
        solvents = []
        sget = self.request.get_all("solvent")
        for s in sget:
            name = ""
            for i in s_var:
                if str(s) == i[0]:
                    name=i[1][0]
                    i[1][1]=True
            solvents.append([name, str(s)])
        for o in o_var:
            d = str(self.request.get(o[1]))
            if d != "":
                valid, error = parse_formula(d, error)
                if valid:
                    solvents.append(["",d])
                    o[0]=d
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

        if exp == False:
            #want normal value
            if solvents == []:
                self.response.set_cookie('s', "")
                self.response.set_cookie('e', "")
                self.response.set_cookie('r', "")
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
            self.response.set_cookie('r', "")
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
            t_var['solvent_variables']=s_var
            t_var['other_variables']=o_var
            self.render_front(t_var)

app = webapp2.WSGIApplication([('/ea/?', EaMainPage),
                               ('/ea/results/?',EaResultHandler),
                               ('/ea/help/?', EaHelpHandler),
                               ('/about/?', AboutHandler),
                               ('/contact/?', ContactHandler),
                               ('/', MainRedirectHandler)
                               ], debug=True)

