## Curve Fitting App

This Curve Fitting App, built with Python and Streamlit, allows users to visualize and analyze data through various curve-fitting techniques. The app supports manual data entry and CSV uploads, enabling users to fit curves such as Polynomial, Exponential, Natural Logarithmic, and Statistical Distributions to their data.

## Features:

### Interactive Data Entry:

 - Manual input of x and y values.
 - Upload CSV files to import datasets.
 - Rename chart titles and axes.

### Curve Fitting Options:

 - Polynomial Fit: Fit data to a polynomial of user-defined degree.
 - Exponential Fit: Fit data to an exponential curve (y = ae^(bx)).
 - Natural Logarithmic Fit: Fit data to a logarithmic curve (y = a + b ln(x)).
 - Statistical Distribution Fit: Visualize data distributions with Gaussian curves.

### Error Analysis:

 - Calculates Maximum Error, Minimum Error, and Mean Absolute Error (MAE) for fitted curves.
 - Displays error bands to visualize the range of deviation.

### Dynamic Plotting:

 - Scatter plots of input data.
 - Fitted curves overlaid with error bands.
 - Histogram and Gaussian bell curves for statistical distributions.
 - Getting Started

## Prerequisites

### Ensure the following Python libraries are installed:

 - streamlit
 - numpy
 - matplotlib
 - pandas

You can install these dependencies using pip:

 - bash
 - pip install streamlit numpy matplotlib pandas
 - Running the App
 - Clone the repository or download the code.
 - Navigate to the directory containing the script.
 - Run the app using Streamlit:
 - bash
 - streamlit run curve_fitting_app.py
 - The app will open in your default web browser.

## Usage
### Data Entry:

Use the manual entry mode to input individual data points or upload a CSV file containing two columns for x and y values.
View and edit your data points dynamically.

### Curve Fitting:

Select the desired curve-fitting method from the dropdown menu.
Adjust parameters like polynomial degree, error accuracy, and more.
Visualize the fitted curve alongside the original data.
Statistical Distribution:

Switch to the Statistical Distribution mode to analyze data histograms and Gaussian distributions.
Error Metrics:

View detailed error metrics for fitted curves.

### Example CSV Format
The uploaded CSV file should contain at least two columns:

csv
x_values,y_values
1,2.3
2,3.8
3,6.1
4,7.5

## Known Limitations
 - Exponential Fit: Requires all y values to be positive.
 - Logarithmic Fit: Requires all x values to be positive.
 - Limited to one dataset at a time.

## Future Enhancements
 - Support for additional curve types and fitting methods.
 - Improved user interface for managing datasets.
 - Export options for fitted curves and plots.

## License
This project is licensed under the MIT license. 

## Acknowledgments
 - Built using Streamlit.
 - Thanks to the Python and data science community for their support and online resources.
