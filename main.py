from flask import Flask, render_template, request, send_from_directory
from flask_login import LoginManager, login_user, current_user
import requests
import tools
import user
import uuid

application = Flask(__name__, static_url_path='')
application.secret_key = ''
kibana_url = ""
grafana_url = ""
domain = ""
login_manager = LoginManager()
login_manager.init_app(application)

@login_manager.user_loader
def load_user(user_id):
    person = user.User(user_id)
    return person


@application.route('/<subdir>/<path:path>')
def kibana_get(path, subdir):
    #this way we check the db only once
    auth = current_user.is_authenticated

    if auth:
        print "User is authed, proxying to kibana for " + path
        response = \
            tools.parse_proxy_request(request, \
                                      kibana_url + subdir + "/" + path, \
                                      "get", \
                                      True)
        print "Response from Elastic to GET " + str(response)
        return tools.send_to_user(response)
    else:
        return render_template('sorry.html')


@application.route("/<subdir>/<path:path>", methods=["POST"])
def kibana_post(path, subdir):
    print "someone is trying to talk to elasticsearch " + path + " <"
    auth = current_user.is_authenticated
    if auth and not tools.allowed(path, request):
        print "data for disallowed post"
        print request.data
        return render_template('sorry.html')
    elif auth:
        response = \
            tools.parse_proxy_request(request, \
                                      kibana_url + subdir + "/"+ path \
                                      ,"post"
                                      ,True)
        print "Response from Elastic to POST " + str(response)
        return tools.send_to_user(response)
    else:
        print "user is not authed"
        return render_template('capcha.html')

@application.route("/<subdir>/<path:path>", methods=["PUT"])
def kibana_put(path, subdir):
    print "someone is trying to talk to elasticsearch " + path + " <"
    auth = current_user.is_authenticated
    if auth and not tools.allowed(path, request):
        print "data for disallowed put"
        print requests.data
        return render_template('sorry.html')
    elif auth:
        response = \
            tools.parse_proxy_request(request, \
                                      kibana_url + subdir + "/"+ path \
                                      ,"put"
                                      ,True)
        print "Response from Elastic to PUT " + str(response)
        return tools.send_to_user(response)
    else:
        return render_template('sorry.html', grafana_url=grafana_url)

@application.route("/<subdir>/<path:path>", methods=["DELETE"])
def kibana_delete(path, subdir):
    print "someone is trying to talk to elasticsearch " + path + " <"
    auth = current_user.is_authenticated
    if auth and not tools.allowed(path, request):
        print "data for disallowed delete"
        print request.data
        return render_template('sorry.html')
    elif auth:
        response = \
            tools.parse_proxy_request(request, \
                                      kibana_url + subdir + "/"+ path \
                                      ,"delete"
                                      ,True)
        print "Response from Elastic to DELETE " + str(response)
        return tools.send_to_user(response)
    else:
        return render_template('sorry.html', grafana_url=grafana_url)


@application.route("/shorten", methods=["POST"])
def kibana_shorten():
    print "someone is trying to shorten a link"
    auth = current_user.is_authenticated
    if auth:
        response = \
            tools.parse_proxy_request(request, \
                                      kibana_url + "shorten" \
                                      ,"post"
                                      ,False)
        print "Response from Elastic" + str(response)
        return tools.send_to_user(response)
    else:
        return render_template('capcha.html', grafana_url=grafana_url)

@application.route("/goto/<short>")
def kibana_unshorten(short):
    auth = current_user.is_authenticated

    if auth:
        print "short request to proxy " + str(request.headers)
        response = \
            tools.parse_proxy_request(request, \
                                      kibana_url + "goto/" + short, \
                                      "get", \
                                      True)
        print "Response from Elastic to short GET " + str(response.headers)
        return tools.send_to_user(response)
    else:
        return render_template('sorry.html')

@application.route('/')
def default():
    print "you have reached the root directory, how can I help you?"
    if current_user.is_authenticated:
        response = requests.get(kibana_url, stream = True)
        return tools.send_to_user(response)
    else:
        return render_template('capcha.html', grafana_url=grafana_url)

@application.route("/submit", methods=["POST"])
def submit():
    print "should only see this when submitting capcha"
    if tools.verify_captcha(request.form['g-recaptcha-response']):
        # SUCCESS
        user_obj = user.User(str(uuid.uuid4()), True)
        login_user(user_obj)
        return render_template('thanks.html')
        pass
    else:
        # FAILED
        return render_template('sorry.html', grafana_url=grafana_url)
        pass


#TODO DO NOT use this in prod, very very slow, move to Nginx
# this is *supposedly* acceptible using uwsgi, we shall see
@application.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)
@application.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)
@application.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)



if __name__ == "__main__":
    application.run(debug=True)
