import os
import webapp2
import jinja2
import logging
from logging.handlers import RotatingFileHandler
from ast import literal_eval
from flask import Flask, render_template, request, make_response, redirect
from flask import url_for, send_from_directory
from script.nm_to_rgb import wavelength_to_rgb
from script.solvent_correct import get_ea, solvent_calculate  # Import the calculator
from script.chemcalc_utilities import *
from PIL import Image
#from app import app

app = Flask(__name__)
#app.debug = True

if not app.debug:
    file_handler = logging.FileHandler(filename='/logs/debug.log')
    file_handler.setLevel(logging.DEBUG)
else:
    file_handler = logging.FileHandler(filename='/logs/debug.log')
    file_handler.setLevel(logging.DEBUG)
    
app.logger.addHandler(file_handler)


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

    # Build rendered_results from components.
    rendered_results['exp'] = rexp
    rendered_results['solvent'] = sresult
    return rendered_results


@app.route('/about')
@app.route('/about/')
def AboutHandler():
    """Simple about-us handler"""
    return render_template("about.html")


@app.route('/contact')
@app.route('/contact/')
def ContactHandler():
    """Simple Contact-Us handler"""
    return render_template("contact.html")


@app.route('/ea/results')
@app.route('/ea/results/')
def EaResultHandler():
    """Requests calculation, rendering, draw results"""
    solvent = list()
    exp = dict()
    formula = check_secure_val(request.cookies.get('f'))
    if not formula:
        return redirect('/ea?r=ecf')
    fparsed, e = parse_formula(formula, "")
    s = check_secure_val(request.cookies.get('s'))
    if s:
        solvent = literal_eval(s)
    elif s is None:
        return redirect('/ea?r=ecs')
    e = check_secure_val(request.cookies.get('e'))
    if e:
        exp = dict(literal_eval(e))
    elif e is None:
        return redirect('/ea?r=ece')

    if formula == "":
        return redirect('/ea?r=nf')
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
                       'mmass': rendered_results['mmass'],
                       }
    return render_template("results.html", **template_values)
                       #    formula=formula,
                       #    rtype = rendered_results['rtype'],
                       #    exp = rendered_results['exp'],
                       #    solvent = rendered_results['solvent'],
                       #    diff = rendered_results['diff'],
                       #    result_formula = rendered_results['result_formula'],
                       #    mmass = rendered_results['mmass']
                       #)


@app.route('/ea/help')
@app.route('/ea/help/')
def EaHelpHandler():
    """Simple help handler"""
    return render_template("eahelp.html")


@app.route('/ea', methods=['POST', 'GET'])
@app.route('/ea/', methods=['POST', 'GET'])
def EaMainPage():
    """Main page. Handles form POST, and flagged returns (errors, etc.)"""

    if request.method == 'POST':
        """Process the form"""
        error = ""
        o_var = [["", "other1"],
                 ["", "other2"],
                 ["", "other3"]
                 ]
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
                 ["CH3CH3SO", ["DMSO", False]]
                 ]
        e_var = [["C", "exp_c", ""],
                 ["H", "exp_h", ""],
                 ["N", "exp_n", ""],
                 ["O", "exp_o", ""],
                 ["S", "exp_s", ""],
                 ["P", "exp_p", ""],
                 ["F", "exp_f", ""],
                 ["Cl", "exp_cl", ""],
                 ["Br", "exp_br", ""],
                 ["I", "exp_i", ""]
                 ]
        t_var = {"formula": "", "exp_variables": e_var,
                 "error": "", "solvent_variables": s_var,
                 "other_variables": o_var}
        solvents = []

        resp = make_response(redirect('ea/results'))

        sget = request.form.getlist("solvent")
        for s in sget:
            name = ""
            for i in s_var:
                if str(s) == i[0]:
                    name = i[1][0]
                    i[1][1] = True
            solvents.append([name, str(s)])
        for o in o_var:
            d = str(request.form.get(o[1]))
            if d != "":
                valid, error = parse_formula(d, error)
                if valid:
                    solvents.append(["", d])
                    o[0] = d
        formula = request.form.get("formula")
        if not formula:
            error = error + "You need to enter a formula. "
        else:
            valid_formula, error = parse_formula(formula, error)

        exp = False
        for e in e_var:
            e[2] = str(request.form.get(e[1]))
            if not is_floatable(e[2]) and e[2] != "":
                error = error + "Not a number error for Experimental %s. " % e[0]
            elif e[2] != '':
                exp = True

        if exp is False:
            #want normal value
            if solvents == []:
                resp.set_cookie('f', make_secure_val(formula))
                return resp
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
            resp.set_cookie('f', make_secure_val(formula))
            resp.set_cookie('s', make_secure_val(solvents))
            resp.set_cookie('e', make_secure_val(experimentals))
            return resp

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
            resp = make_response(render_template("eaform.html", **t_var))
            return resp

    else:  # GET
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
        r = request.args.get('r')
        if r:
            if r == 'nf':
                error = "You need to enter information before getting results. "
            elif r == "r":
                for s in solvent_list:
                    s[1][1] = False
            elif r == "c":
                formula = check_secure_val(request.cookies.get('f'))
                s = check_secure_val(request.cookies.get('s'))
                if s:
                    sol = literal_eval(s)
                    for s in sol:
                        for t in solvent_list:
                            if s[0] == t[1][0]:
                                t[1][1] = True
                e = check_secure_val(request.cookies.get('e'))
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

        template_values = {"formula": formula,
                           "exp_variables": e_var,
                           "solvent_variables": solvent_list,
                           "error": error,
                           "other_variables": other_variables,
                           }
        resp = make_response(render_template("eaform.html", **template_values))
        resp.set_cookie('f', "")
        resp.set_cookie('s', "")
        resp.set_cookie('e', "")
        return resp


@app.route('/')
def HomeHandler():
    """Homepage"""
    return render_template("home.html")


@app.route('/colour/<wavelength>', methods=['POST', 'GET'])
@app.route('/color/<wavelength>', methods=['POST', 'GET'])
@app.route('/colour/', methods=['POST', 'GET'])
@app.route('/colour', methods=['POST', 'GET'])
@app.route('/color/', methods=['POST', 'GET'])
@app.route('/color', methods=['POST', 'GET'])
def ColourDrawer(wavelength=None):
    """Put up the form to get info for colour showing."""
    if request.method == 'POST':
        wavelength=request.form.get('wavelength')
        if int(wavelength)<380 or int(wavelength)>780:
            error = "Visible light is between 380 and 780 nm."
            resp = render_template('colour.html', error=error)
            return resp
        elif not is_numeric(wavelength):
            error = "Form requires a number for wavelength lookup."
            resp = render_template('colour.html', error=error)
            return resp
        if 'color' in request.base_url:
            return redirect('/color/%s' % wavelength)
        else:
            return redirect('/colour/%s' % wavelength)
    else:
        if wavelength:
            #results
            if int(wavelength)<380 or int(wavelength)>780:
                error = "Visible light is between 380 and 780 nm."
                resp = render_template('colour.html', error=error)
                return resp
            elif not is_numeric(wavelength):
                error = "Form requires a number for wavelength lookup."
                resp = render_template('colour.html', error=error)
                return resp
            logging.debug(wavelength)
            colour = wavelength_to_rgb(wavelength)
            filename = "%s_nm.jgp" % wavelength
            directory = path.join(os.path.dirname(os.path.realpath(__file__)),
                                  'static','wavelength')
            savepath = path.join(directory, filename)
            # don't remake the plot if the file exists. Fails on no file or no dir.
            if not path.isfile(savepath):
                im = Image.new('RGB',
                               (200, 200),
                               (colour[0], colour[1], colour[2]))
                #ensure the path is prepared
                if not path.exists(directory):
                    makedirs(directory)
                im.save(savepath)
            template_values = {'plot_filename':filename,
                               'wavelength':wavelength,
                               'before':int(wavelength)-1,
                               'after':int(wavelength)+1,
                               }
            resp = make_response(render_template("colour.html",
                                                 **template_values))
            return resp
        else:
            return render_template('colour.html')


@app.route('/isotopes/<relement>')
@app.route('/isotopes/')
@app.route('/isotopes')
def IsotopeHandler(relement=None):
    e = request.args.get('e')
    f = request.args.get('f')
    # Have to decide some way to handle mixed input. Do both!
    isotopes = list ()
    selected_elements = False
    if relement in ELEMENTS:
        return redirect('/isotopes?e=%s' % relement)
        
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
    isotopes = sorted(isotopes,
                      key=lambda isotopes: (isotopes[2], isotopes[3][0]))
    template_values = {"elements": isotopes,
                       "element_name": element_names,
                       "element_symbol": element_symbols,
                       "hclass": "isotopes",
                       }
    return render_template("mass_table.html", **template_values)


@app.route('/isotopes/help')
@app.route('/isotopes/help/')
def IsotopeHelpHandler():
    """Simple Isotope Help Handler"""
    return render_template("isotopehelp.html")


@app.route('/sitemap')
@app.route('/sitemap/')
def SitemapHandler():
    """Return the sitemap.html page"""
    return render_template("sitemap.html")

@app.route('/exact-mass/<informula>', methods=['POST', 'GET'])
@app.route('/exact-mass/', methods=['POST', 'GET'])
@app.route('/exact-mass', methods=['POST', 'GET'])
def ExactMassDistribute(informula=None):
    """Put up the form to get info for exact mass."""
    if request.method == 'POST':
        formula=request.form.get('formula')
        response, error = parse_formula(str(formula), "")
        if error:
            resp = render_template('exact-mass.html', error=error)
            return resp
        return redirect('/exact-mass/%s' % shorten_formula(response))
    else:
        if informula:
            #results
            formula, error = parse_formula(str(informula), "")
            if error:
                resp = render_template('exact-mass.html', error=error)
                return resp
            logging.debug(formula)
            sformula = shorten_formula(formula)
            isotopes = isotope_distribute(formula)
            name = md5(str(formula)).hexdigest()
            filename = "%s.png" % name
            directory = path.join(os.path.dirname(os.path.realpath(__file__)),'static','plots')
            savepath = path.join(directory, filename)            # don't remake the plot if the file exists. Fails on no file or no dir.
            if not path.isfile(savepath):
                plt = plot_isotopes(isotopes, sformula)
                #ensure the path is prepared
                if not path.exists(directory):
                    makedirs(directory)
                plt.savefig(savepath, bbox_inches='tight')
            
            template_values = {'plot_filename':filename,
                               'isotopes':isotopes,
                               'formula':sort_formula(formula),
                               }
            resp = make_response(render_template("mass-distribution.html",
                                                 **template_values))
            return resp
        else:
            return render_template('exact-mass.html')

@app.route('/hire-me')
@app.route('/give-me-a-job')
def HiremeHandler():
    """Return the sitemap.html page"""
    return render_template("hireme.html")

@app.route('/robots.txt')
@app.route('/sitemap.xml')
@app.route('/favicon.ico')
@app.route('/BingSiteAuth.xml')
@app.route('/resume.pdf')
def static_from_root():
    """Serve static sitemap.xml and robots.txt"""
    return send_from_directory(app.static_folder, request.path[1:])


@app.errorhandler(404)
def page_not_found(e):
    """Simple 404 error handler"""
    app.logger.info(e)
    resp = make_response(render_template("404.html"))
    resp.set_cookie('f', expires=0)
    resp.set_cookie('s', expires=0)
    resp.set_cookie('e', expires=0)
    return resp, 404

@app.errorhandler(500)
def server_error(e):
    """Simple 500 error handler"""
    app.logger.error(e)
    resp = make_response(render_template("500.html"))
    resp.set_cookie('f', expires=0)
    resp.set_cookie('s', expires=0)
    resp.set_cookie('e', expires=0)
    return resp, 500

if __name__ == "__main__":
    #app.debug = True
    app.run()


