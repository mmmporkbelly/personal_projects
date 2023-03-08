from website import create_app

app = create_app()

if __name__ == '__main__':
    # Run flask app, debug = True means that if changes to code are made, web server will be rerun
    # Take out debug=True in production
    app.run(debug=True)


