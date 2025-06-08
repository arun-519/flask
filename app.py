from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb+srv://arunselvam519:suriya519@cluster0.jgjrq4q.mongodb.net/?retryWrites=true&w=majority")
db = client["college_pages"]
collection = db["pages"]

# Admin panel
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Retrieve data from the form
        header = request.form.get("header")
        header_content = request.form.get("header_content")
        vision = request.form.get("vision")
        mission = request.form.get("mission")
        quality_policy = request.form.get("quality_policy")

        # Save new college page data to MongoDB
        collection.insert_one({
            "header": header,
            "header_content": header_content,
            "vision": vision,
            "mission": mission,
            "quality_policy": quality_policy
        })
        return redirect(url_for('admin'))

    # Fetch all existing pages for admin view
    pages = list(collection.find({}))
    return render_template('admin.html', pages=pages)

# Dynamic college page
@app.route('/page/<page_id>')
def college_page(page_id):
    page = collection.find_one({"_id": ObjectId(page_id)})
    if not page:
        return "Page not found", 404

    return render_template(
        'replica.html',
        header=page['header'],
        header_content=page['header_content'],
        vision=page['vision'],
        mission=page['mission'],
        quality_policy=page['quality_policy']
    )

# Homepage
@app.route('/')
def home():
    pages = list(collection.find({}))
    return render_template('home.html', pages=pages)

if __name__ == '__main__':
    app.run(debug=True)
