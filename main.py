from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField,TimeField,SelectField
from wtforms.validators import DataRequired
import csv

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap=Bootstrap5(app)


class CafeForm(FlaskForm):
    my_choices_coffee = ['☕', '☕☕', '☕☕☕', '☕☕☕☕️', '☕☕☕☕️☕']
    my_choices_wifi = ['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪']
    my_choices_power = ['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌' ]

    cafe = StringField('Cafe name', validators=[DataRequired()])
    URL = URLField(label="Enter URL", validators=[DataRequired()])
    open_time = StringField(label="Enter opening Time e.g 9:30AM",validators=[DataRequired()])
    close_time = StringField(label="Enter closing Time e.g 10PM",validators=[DataRequired()])
    select_coffee_rating = SelectField(label='Coffee Rating',choices=my_choices_coffee,validators=[DataRequired()])
    select_wifi_strength_rating=SelectField(label='Wifi Strength Rating',choices=my_choices_wifi,
                                            validators=[DataRequired()])
    select_power_rating = SelectField(label='Power Socket Availability', choices=my_choices_power,validators=[DataRequired()])

    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('./cafe-data.csv', 'a', encoding='utf-8') as file:
            file.writelines(f"\n{form.cafe.data},{form.URL.data},"
                            f"{form.open_time.data},"
                            f"{form.close_time.data},"
                            f"{form.select_coffee_rating.data},"
                            f"{form.select_wifi_strength_rating.data},"
                            f"{form.select_power_rating.data}")
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
