from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

notes_dict = {}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')

        if title and text:
            notes_dict[title] = text

        return redirect(url_for('notes'))

    return render_template('notes.html', notes=notes_dict)


if __name__ == '__main__':
    app.run(debug=True)