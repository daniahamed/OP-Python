from flask import Flask, request, jsonify, render_template, flash, redirect, url_for

def validate(form_data):
    errors = []

    if not form_data["name"]:
        errors.append("Name is required")

    if not form_data["email"] or "@" not in form_data["email"]:
        errors.append("Email must be in a valid email format")

    if not form_data["password"] or len(form_data["password"]) < 8:
        errors.append("Password must be at least 8 characters long")

    if form_data["password"] != form_data["confirm_password"]:
        errors.append("Passwords do not match")

    if form_data["bio"] and len(form_data["bio"]) < 20:
        errors.append("Bio must be at least 20 characters long")

    if not form_data["terms"]:
        errors.append("You must agree to the terms")

    return errors


app = Flask(__name__)
app.secret_key = "secret-key" 

@app.route("/", methods = ["GET", "POST"])
def func():
    form_data = {
        "name": "",
        "email": "",
        "bio": "",
        "terms": None
    }
    if request.method == "POST":
        form_data = {
            "name": request.form.get("name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "password": request.form.get("password", "").strip(),
            "confirm_password": request.form.get("confirm-password", "").strip(),
            "bio": request.form.get("bio", "").strip(),
            "terms": request.form.get("terms")
        }

        errors = validate(form_data)

        if errors:
            form_data["password"] = ""
            form_data["confirm_password"] = ""
            return render_template("form.html", errors=errors, form_data=form_data)

        flash("Form submitted successfully!")
        return redirect(url_for("func"))

    return render_template("form.html", form_data= form_data)

if __name__ == "__main__":
    app.run(debug=True)
