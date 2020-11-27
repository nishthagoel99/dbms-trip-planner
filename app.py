from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev')

    @app.route('/')
    def index():
        return render_template('base.html')

    @app.route('/register')
    def index():

        return render_template('selectregister.html')

    import user
    app.register_blueprint(user.bp)
    return app
