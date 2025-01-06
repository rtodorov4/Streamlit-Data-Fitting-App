#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 01:05:12 2024

@author: ryanzhu

Name: Curve Fitting App Project
"""
import streamlit as st # type: ignore
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
import pandas as pd # type: ignore


def isnumeric(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


def polynomial_fit(xs, ys, deg):
    deg = int(deg)
    coeffs = np.polyfit(xs, ys, deg=deg)
    y = 0
    equation = 'y ='

    # building the equation with logic because I didn't realize np.polyval was an option at the time of coding TT
    for i in range(len(coeffs)):
        y += coeffs[i]*x**(len(coeffs) - 1 - i)

        # building equation
        if i == 0 or coeffs[i] < 0:
            equation += ' '
        else:
            equation += ' + '
        equation += str(round(coeffs[i], eq_accuracy))
        equation += 'x^'
        equation += str(len(coeffs) - 1 - i)

    # calculating error
    y_pred = np.polyval(coeffs, xs)

    error = ys - y_pred

    max_error = max(abs(error))
    min_error = min(abs(error))
    MAE_error = np.array(abs(error))
    MAE_error = sum(MAE_error) / len(MAE_error)

    return coeffs, equation, max_error, min_error, MAE_error


def natural_logarithmic_fit(xs, ys):
    # log xs
    ln_xs = np.log(xs)  # y = a + b * 'lnx'

    # linear regression
    b, a = np.polyfit(ln_xs, ys, 1)

    # calculating error
    y_pred = a + b * np.log(xs)

    error = ys - y_pred

    max_error = max(abs(error))
    min_error = min(abs(error))
    MAE_error = np.array(abs(error))
    MAE_error = sum(MAE_error) / len(MAE_error)
    return a, b, max_error, min_error, MAE_error


def exponential_fit(xs, ys):
    # ln(y) = ln(a) + b * x
    log_ys = np.log(ys)
    b, ln_a = np.polyfit(xs, log_ys, 1)  # linear fit

    a = np.exp(ln_a)  # convert a back to exp form

    # calculating error
    y_pred = a * np.exp(b * xs)

    error = ys - y_pred

    max_error = max(abs(error))
    min_error = min(abs(error))
    MAE_error = np.array(abs(error))
    MAE_error = sum(MAE_error) / len(MAE_error)
    return a, b, max_error, min_error, MAE_error


# initializing the data value lists and rerun state (not sure how this works tbh but it do)
if 'xs' not in st.session_state:
    st.session_state.xs = []

if 'ys' not in st.session_state:
    st.session_state.ys = []

if 'rerun' not in st.session_state:
    st.session_state.rerun = False

if st.session_state.rerun is True:
    st.session_state.rerun = False
    st.experimental_rerun()

# App title
st.header('Excel (but drunk :3 )', divider='blue')

# Data Entry Header
st.header('Data Entry', divider='blue')

with st.expander(label='Rename Axes or Chart'):
    x_label = st.text_input(label='Name your X axis')
    if x_label == '':
        x_label = 'x values'

    y_label = st.text_input(label='Name your Y axis')
    if y_label == '':
        y_label = 'y values'

    title = st.text_input(label='Name your Chart',)
    if title == '':
        title = 'Your Data'


if st.toggle('Manual Entry') is False:
    cols = st.columns(2, gap='small')
    # spacer
    cols[1].write('')

    with cols[1].form("my-form", clear_on_submit=True):
        file = cols[0].file_uploader(label='CSV file upload', type='csv')
        submitted = st.form_submit_button("Upload selected CSV")

        if submitted and file is not None:
            try:
                df = pd.read_csv(file)

                # Ensure the CSV contains at least two columns
                if len(df.columns) < 2:
                    st.error("The CSV file must have at least two columns for x and y values.")
                else:
                    # Extract the first two columns
                    x_values = df.iloc[:, 0].tolist()
                    y_values = df.iloc[:, 1].tolist()

                    # Check if the values are numeric
                    if all(isnumeric(x) for x in x_values) and all(isnumeric(y) for y in y_values):
                        # Convert to floats and append to session state
                        st.session_state.xs.extend(map(float, x_values))
                        st.session_state.ys.extend(map(float, y_values))
                        success = st.success("Data successfully added!")
                    else:
                        st.error("The CSV file contains non-numeric values in the first two columns.")
            except FileNotFoundError:
                st.error("The specified file was not found. Please check the filename and try again.")
            except Exception as e:
                st.error(f"An error occurred while processing the file: {e}")

    # clear data
    if cols[1].button('Clear Data Set'):
        if len(st.session_state.xs) > 0:
            st.session_state.xs = []
            st.session_state.ys = []
        else:
            st.error('No data to clear')

# manual extnry
else:
    # setting up columns
    cols = st.columns(2, gap='small')

    # setting up entries
    x = cols[0].text_input(label='Enter an x value')
    y = cols[1].text_input(label='Enter a y value')

    # enter key
    if cols[0].button('Add data set'):
        if isnumeric(x) and isnumeric(y):
            st.session_state.xs.append(float(x))
            st.session_state.ys.append(float(y))
        else:
            st.error('invalid data type')

    # delete entry
    if cols[1].button('delete last data set'):
        if len(st.session_state.xs) != 0:
            del st.session_state.xs[-1]
            del st.session_state.ys[-1]
        elif len(st.session_state.xs) == 0:
            st.error('no entries to delete')

# Show Data
with st.expander('Data Points'):
    data = []
    for i in range(len(st.session_state.xs)):
        data.append([st.session_state.xs[i], st.session_state.ys[i]])

    st.write(f'Your data points are: :d {data}')

# Curve fitting
st.header('Curve Fitting', divider='blue')

# selecting the curve to fit
curves_to_fit = ['Polynomial', 'Exponential', 'Natural Logarithmic', 'Statistical Distribution']

# defaulting to least error option
mode = st.selectbox(label='Fit a Curve', options=curves_to_fit)

# plotting the data
fig, ax = plt.subplots()

# convert xs and ys to numpy arrays cause they're weird af rn
xs = np.array(st.session_state.xs, dtype='float')
ys = np.array(st.session_state.ys, dtype='float')

eq_accuracy = 5
max_error = None
min_error = None
MAE_error = None

if len(xs) > 0:

    # redefine cols for below Curve Fitting Header
    cols = st.columns(2)

    if mode == 'Statistical Distribution':

        if cols[0].toggle('Use x values'):
            dist = xs
            dist_label = x_label
        else:
            dist = ys
            dist_label = y_label

        if cols[1].toggle('Show Instance Count'):
            try:
                # compute mean and stdev
                mean = np.mean(dist)
                std_dev = np.std(dist)

                # Plot histogram and gather bin width data (tbh no idea what patches are lol)
                counts, bin_edges, patches = ax.hist(dist, bins=30, color='gray', edgecolor='black', label='Data Histogram')

                # compute bin width and total instances
                bin_width = bin_edges[1] - bin_edges[0]
                total_instances = len(dist)

                # generate bell curve values: 1 / (std_dev * √(2pi)) * e**(-0.5[(x - mean)/(std. dev)]**2)
                x = np.linspace(min(dist), max(dist), 1000)
                bell_curve = (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev) ** 2)

                # scale bell curve to instance count
                scaled_bell_curve = bell_curve * total_instances * bin_width

                # Plot bell curve
                ax.plot(x, scaled_bell_curve, color='mediumseagreen', lw=2, label='Gaussian Distribution (Bell Curve)')

                # Add legend and labels
                ax.legend()
                st.write(f"Mean: {round(mean, eq_accuracy)} | Standard Deviation: {round(std_dev, eq_accuracy)}")

                # labeling the axes
                ax.grid(True)
                ax.set_xlabel(dist_label)
                ax.set_ylabel('Instance Count')
                ax.set_title(f'Statistical Distribution of {dist_label} (Instance Count)')
            except Exception as e:
                st.error(f'Error in Statistical Distribution Fitting: {e}')
        else:
            try:
                # compute mean and stdev
                mean = np.mean(dist)
                std_dev = np.std(dist)

                # generate bell curve values
                x = np.linspace(min(dist), max(dist), 1000)
                bell_curve = (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev) ** 2)

                # Plot histogram
                ax.hist(dist, bins=30, color='gray', density=True, edgecolor='black', label='Data Histogram')

                # Plot bell curve
                ax.plot(x, bell_curve, color='mediumseagreen', lw=2, label='Gaussian Distribution (Bell Curve)')

                # Add legend and labels
                ax.legend()
                st.write(f"Mean: {round(mean, eq_accuracy)} | Standard Deviation: {round(std_dev, eq_accuracy)}")

                # labeling the axes
                ax.grid(True)
                ax.set_xlabel(dist_label)
                ax.set_ylabel('Probability Density')
                ax.set_title(f'Statistical Distribution of {dist_label} (Probability Density)')
            except Exception as e:
                st.error(f'Error in Statistical Distribution Fitting: {e}')
    else:
        ax.scatter(xs, ys, color='darkblue')

        # making axis limits
        buffer = 2
        max_x = max(xs, default=0)
        max_y = max(ys, default=0)

        min_x = min(xs, default=0)
        min_y = min(ys, default=0)

        ax.set_xlim([min_x - buffer, max_x + buffer])
        ax.set_ylim([min_y - buffer, max_y + buffer])

        # adding labels
        ax.grid(True)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)

        # adding axis lines
        x_ax = np.linspace(min_x - buffer, max_x + buffer, 5)
        y_ax = np.linspace(min_y - buffer, max_y + buffer, 5)
        zeros = np.zeros(5)
        ax.plot(x_ax, zeros, color='black')
        ax.plot(zeros, y_ax, color='black')

        if len(xs) >= 2:
            # polynomials
            if mode == 'Polynomial':
                deg = st.number_input('Input a Degree', min_value=0, value=1, step=1)
                try:
                    x = np.linspace(min_x - buffer, max_x + buffer, 1000)
                    coeffs, equation, max_error, min_error, MAE_error = polynomial_fit(xs, ys, deg)

                    # plot MAE error range
                    error_line_top = np.polyval(coeffs, x) + MAE_error
                    error_line_bottom = np.polyval(coeffs, x) - MAE_error
                    ax.fill_between(x, error_line_top, error_line_bottom, color='red', alpha=0.25, label='Mean Absolute Error')

                    st.write(f"$${equation}$$")
                    ax.plot(x, np.polyval(coeffs, x), color='mediumseagreen', label=f'Polynomial Fit (of degree {deg})')
                    ax.legend()

                except Exception as e:
                    st.error(f'Invalid Degree Input: {e}')

            elif mode == 'Exponential':
                try:
                    # ln(y) = ln(a) + b * x
                    # ensure y values are positive
                    if any(ys <= 0):
                        st.error('Nuh uh. Data set outside of range (y values must be greater than 0)')
                    else:

                        a, b, max_error, min_error, MAE_error = exponential_fit(xs, ys)

                        # Generate curve points
                        x = np.linspace(min_x - buffer, max_x + buffer, 1000)
                        y = a * np.exp(b * x)

                        # plot MAE error range
                        error_line_top = y + MAE_error
                        error_line_bottom = y - MAE_error
                        ax.fill_between(x, error_line_top, error_line_bottom, color='red', alpha=0.25, label='Mean Absolute Error')


                        # Display equation and plot
                        st.write(f'$y = {round(a, eq_accuracy)} * e^{{{round(b, eq_accuracy)}}} * x$')
                        ax.plot(x, y, color='mediumseagreen', label='Exponential Fit')
                        ax.legend()

                except Exception as e:
                    st.error(f'Error in Exponential Fitting: {e}')

            elif mode == 'Natural Logarithmic':
                try:
                    if any(xs <= 0):
                        st.error('Nuh uh. Data set outside of domain (x values must be greater than 0')
                    else:

                        a, b, max_error, min_error, MAE_error = natural_logarithmic_fit(xs, ys)

                        # Generate Curve Points
                        x = np.linspace(min_x - buffer, max_x + buffer, 1000)
                        y = a + b * np.log(x)

                        # plot MAE error range
                        error_line_top = y + MAE_error
                        error_line_bottom = y - MAE_error
                        ax.fill_between(x, error_line_top, error_line_bottom, color='red', alpha=0.25, label='Mean Absolute Error')


                        # Display Equation and plot
                        st.write(f"$y = {round(a, eq_accuracy)} + {round(b, eq_accuracy)}lnx$")
                        ax.plot(x, y, color='mediumseagreen', label='Natural Logarithmic Fit')
                        ax.legend()
                except Exception:
                    st.error('Error in Natural Logarithmic Fitting')
        else:
            st.error('Nope. Need at least two data points to fit curves ;-;')

st.pyplot(fig)

if max_error is not None and min_error is not None and MAE_error is not None:
    st.write(f'Maximum Error is approx. {round(max_error, eq_accuracy)} units')
    st.write(f'Minimum Error is approx. {round(min_error, eq_accuracy)} units')
    st.write(f'Mean Absolute Error is approx {round(MAE_error, eq_accuracy)} units')

# error

