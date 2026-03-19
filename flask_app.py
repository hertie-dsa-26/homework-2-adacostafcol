from flask import Flask, render_template, request
from circle import Circle
from helper import perform_calculation, convert_to_float

app = Flask(__name__)  # create the instance of the flask class


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/calculate', methods=['GET', 'POST'])  # associating the GET and POST method with this route
def calculate():
    if request.method == 'POST':
        # using the request method from flask to request the values that were sent to the server through the POST method
        value1 = request.form['value1']
        value2 = request.form['value2']
        operation = str(request.form['operation'])

        # make sure the input is one of the allowed inputs (not absolutely necessary in the drop-down case)
        if operation not in ['add', 'subtract', 'divide', 'multiply']:
            return render_template('calculator.html',
                                   printed_result='Operation must be one of "add", "subtract", "divide", or "multiply".')

        try:
            value1 = convert_to_float(value=value1)
            value2 = convert_to_float(value=value2)
        except ValueError:
            return render_template('calculator.html', printed_result="Cannot perform operation with this input")

        try:
            result = perform_calculation(value1=value1, value2=value2, operation=operation)
            return render_template('calculator.html', printed_result=str(result))

        except ZeroDivisionError:
            return render_template('calculator.html', printed_result="You cannot divide by zero")

    return render_template('calculator.html')


@app.route('/circle', methods=['GET', 'POST'])
def circle_calculator():
    result = None
    error = None
    
    if request.method == 'POST':
        try:
            radius_input = request.form['radius']
            radius = float(radius_input)
            
            if radius <= 0: 
                raise ValueError("Yo! The radius must be a positive number!!!!")
            
            circle = Circle(radius)
            perimeter = circle.perimeter() 
            area = circle.area()           
            
            result = {
                'radius': radius,
                'perimeter': round(perimeter, 2), 
                'area': round(area, 2)              
            }
            
        except ValueError as e:  
            error = f"Error: {str(e)}"
            
        except Exception as e:    
            error = f"Error unexpected: {str(e)}"
    
    return render_template('circle.html', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)





             

                          

