# Trendify README and User Guide

**Table of Contents**

- [About this guide](#about-this-guide)
	- [What is Trendify?](#what-is-trendify)
	- [Who is this guide for?](#who-is-this-guide-for)
- [Navigating Trendify](#navigating-trendify)
- [Understanding Trendify’s workflow](#understanding-trendifys-workflow)
- [Opening your data on Trendify](#opening-your-data-on-trendify)
- [Loading an existing model on Trendify](#loading-an-existing-model-on-trendify)
- [Preprocessing your data](#preprocessing-your-data)
	- [Handling null values in your data](#handling-null-values-in-your-data)
	- [Methods for handling null values in your data](#methods-for-handling-null-values-in-your-data)
- [Choosing your variables and creating a model](#choosing-your-variables-and-creating-a-model)
	- [Choosing your input columns](#choosing-your-input-columns)
	- [Choosing your output column](#choosing-your-output-column)
- [Creating a description for your model](#creating-a-description-for-your-model)
- [Creating a model](#creating-a-model)
- [Making predictions](#making-predictions)
- [Viewing and interacting with your model graph](#viewing-and-interacting-with-your-model-graph)
	- [Saving an image or PDF of your model graph](#saving-an-image-or-pdf-of-your-model-graph)
- [Saving Your Model](#saving-your-model)
- [Glossary](#glossary)

# **About this guide**

This guide is intended to help you quickly get started with Trendify, a user-friendly tool for building linear regression models and making predictions based on your data. Whether you're a student, a beginner analyst, or a professional with limited technical knowledge, this guide will walk you through the steps of using Trendify. By following this guide, you will:

* Learn how to upload your data and progress through the preprocessing stage.  
* Understand how to select the appropriate input and output variables for your model.  
* Gain the skills to create a model and generate predictions based on your data.  
* Be able to view and interpret the results of your predictions.

## **What is Trendify?**

Trendify is a software tool that simplifies the process of applying linear regression models to data analysis. It allows users to upload datasets, clean them, select variables, create models, and make predictions. The software is designed with accessibility in mind, ensuring that individuals without deep technical expertise can use it to analyze data and make informed decisions. By utilizing machine learning techniques, Trendify enables users to predict outcomes, such as estimating prices or other values, based on input variables.

## **Who is this guide for?**

This guide is intended for a diverse range of users, including those with limited technical expertise in data analysis, as well as those looking to deepen their understanding of machine learning and regression models. Regardless of your experience level, this guide will help you effectively navigate Trendify, create accurate models, and make data-driven predictions.

Refer to [Table 1](#table1) for an overview of who this guide is intended for and why it is relevant to each group.

| User type | Explanation |
| :---- | :---- |
| Student | Ideal for learning about linear regression, machine learning, or data analysis. |
| Beginner Analysts | Perfect for exploring data analysis without extensive programming knowledge. |
| Professionals | Suitable for performing simple data analysis and making predictions based on datasets. |

<p id="table1"><strong>Table 1</strong>: User types and how this guide applies to them</p>

# **Navigating Trendify**

Navigating Trendify is designed to be intuitive, with a clear and user-friendly interface that guides users through the entire process of data analysis. Whether you're uploading data, choosing variables, or creating a model, each panel is organized to make your experience seamless.

Refer to [Figure 1](#figure1) and [Table 2](#table2) for an overview of the main components of Trendify's interface.

![The Trendify interface and each of its panels](https://imgur.com/W8pK7D1.png)
<p id="figure1"><strong>Figure 1</strong>: The Trendify interface and each of its panels<p>

| Number | Panel | Purpose |
| :---- | :---- | :---- |
| 1 | Model Creation | Contains all the buttons used to analyze data, build a model, and save a model. |
| 2 | Handle Null Values | A dropdown menu that is part of preprocessing data. Contains the methods for handling null (nan) values in data. |
| 3 | Data Display | The area where the data you open on Trendify is displayed. |
| 4 | Model Description | Contains information about your model (See [Table 4](#bookmark=id.d225b91ivqho) for the complete details). |

<p id="table2"><strong>Table 2</strong>: Panels on Trendify’s interface and their purpose<p>

# **Understanding Trendify’s workflow** 

From when you first open Trendify, the interface is designed to guide you step-by-step through the process of building and using a linear regression model. Initially, many features in the workspace are greyed-out, to ensure that you complete tasks in the correct sequence. This approach helps prevent errors and streamlines your workflow.  
First you must upload your data or load an existing model. For detailed instructions on these steps, refer to [Opening your data on Trendify](#opening-your-data-on-trendify) and [Loading an existing model on Trendify](#loading-an-existing-model-on-trendify). Once your file or model is loaded, more features and options become accessible, allowing you to progress seamlessly through preprocessing your data and building your model.

For a visual representation of Trendify’s workflow, refer to the flowchart in [Figure 2](#figure2).

![Flowchart illustrating the sequence of functions in Trendify](https://i.imgur.com/l5nP8Rv.png)
<p id="figure2"><strong>Figure 2</strong>: Flowchart illustrating the sequence of functions in Trendify<p>

# **Opening your data on Trendify** 

Trendify analyzes spreadsheets with numerical data organized into columns to build linear regression models. These models are useful for identifying relationships and trends in data, as well as for making predictions. Trendify can make linear regression models with the following data file types:

* CSV (Comma-Separated Value) files  
* XLSX (Excel) files  
* SQLite files

**To open your data on Trendify**

1. Select **OPEN FILE**.  
   The **Select File** dialog opens.  
2. Choose the data file you want to open, and then select **Open**.  
   Your data appears in the Data Display panel. 

# **Loading an existing model on Trendify** 

You can load models you have previously created and saved on Trendify to make predictions without having to preprocess your data and reselect variables.

Trendify can load existing models with the following data types:

* pkl (pickle) files  
* joblib files

**To load an existing model**

1. Select **Load Model**.  
   The **Select Model File** dialog opens.  
2. Choose the model file you want to open, and then select **Open**.  
   The **Model Loaded** dialog opens.  
3. Select **OK**.  
   Your model is loaded and its information is displayed in the Model Description panel.

# **Preprocessing your data**

Preprocessing data allows Trendify to prepare the data you uploaded to effectively build linear regression models. This process identifies gaps in the data, called null values, that can prevent regression models from working. 

**To preprocess your data**

1. Select **Preprocess Data**.  
  The **Null Values Detected** dialog opens. If null values are found, the column name containing the null values and the amount of null values are displayed (see [Figure 3](#figure3).   
  Select **OK**. 
  2. Choose a method to [handle the null values in your data](#handling-null-values-in-your-data).

![The Null Values Detected dialog showing column name (total_bedrooms) of where null values are found and the amount of null values found (207)](https://imgur.com/zDKjUHi.png)
<p id="figure3"><strong>Figure 3</strong>: The <strong>Null Values Detected</strong> dialog showing column name (total_bedrooms) of where null values are found and the amount of null values found (207)<p>

## **Handling null values in your data** 

Trendify can handle null values (nan) in your data by either deleting rows with null values or filling them with calculated values. For example, you can fill null values with the mean of the column (see [Figure 4](#figure4) and [Figure 5](#figure5). To understand the available methods and determine which option works best for your data, refer to [Methods for handling null values in your data](#methods-for-handling-null-values-in-your-data).

**To delete rows with null values**

1. Go to **Handle Null Values**, and then select **Delete rows with nulls**.  
   The **Caution** dialog opens.  
2. Select **Yes**.  
   The **Rows Deleted** dialog opens.  
3. Select **OK**.   
   The rows in your data with null values are deleted.

**To fill null values with the mean**

1. Go to **Handle Null Values**, and then select **Fill with mean**.  
   The **Caution** dialog opens.  
2. Select **Yes**.  
   The **Filled with mean** dialog opens.  
3. Select **OK**.   
   The null values in your data are filled with the mean of their respective columns (see [Figure 5](#figure5).

**To fill null values with the median**

1. Go to **Handle Null Values**, and then select **Fill with median**.  
   The **Caution** dialog opens.  
2. Select **Yes**.  
   The **Filled with median** dialog opens.  
3. Select **OK**.  
   The null values in your data are filled with the median of their respective columns.

**To fill null values with a constant**

1. Go to **Handle Null Values**, and then select **Fill with constant**.  
   A text box appears in **Handle Null Values**.  
2. Enter the number you want to replace null values with, and then select your **Enter** key.  
   The **Caution** dialog opens.  
3. Select **Yes**.  
   The **Filled with constant** dialog opens.  
4. Select **OK**.  
   The null values in your data are filled with the constant you entered.

## **Methods for handling null values in your data** 

Trendify provides several methods to handle null values in your data, each with specific kind of data they are more suited for (see [Table 3](#table3). Choosing the appropriate method for your data ensures accurate, reliable data analysis and reduces the risk of bias.

| Method | Function | Use case |
| :---- | :---- | :---- |
| Deleting rows | Removes entire rows that contain null values. | When removing rows will not significantly impact the analysis, for example: Large datasets with thousands of rows or more. Very small percentage of rows have null values. |
| Filling with mean | Replaces null values with the average of all non-missing values in the column. | Numerical data Evenly distributed data No extreme outliers in data |
| Filling with median | Replaces null values with the middle value of sorted data in the column. | Numerical data Has outliers or skewed distribution |
| Filling with constant | Replaces null values with a fixed value. | Categorical data You want to create a “missing” or “other” category that is represented by a numerical value |

<p id="table3"><strong>Table 3</strong>: The methods of handling null values, their function, and their most suitable use cases<p>

![Raw data with a null value in total_bedrooms column](https://imgur.com/DbKnNO3.png)  
<p id="figure4"><strong>Figure 4</strong>: Raw data with a null value in total_bedrooms column<p>

![Preprocessed data where null value is filled with the mean of the total](https://imgur.com/GAtrvjN.png)  
<p id="figure5"><strong>Figure 5</strong>: Preprocessed data where null value is filled with the mean of the total_bedrooms column<p>

# **Choosing your variables and creating a model** 

Input and output variables are the foundation of linear regression models. Input variables (independent variables) are the factors you believe influence an outcome, while the output variable (dependent variable) represents the result or response to those factors. By selecting the right input and output variables, you can build a model that identifies patterns and relationships within your data.

## **Choosing your input columns** 

To define your model’s independent variables, you need to select the input columns. Trendify will use these columns as the independent variables to determine how they influence the output variable.  You can choose up to three input columns, though only models with one or two input columns can be visualized in 2D or 3D graphs.

**To choose your input columns**

1. Select **Select Input Columns**.  
   The **Select Columns** dialog opens.  
2. Choose the columns you want to use as input variables, then select Confirm Selection.   
   The Columns Selected dialog opens, stating your chosen input columns.  
3. Select **OK**.   
   The selected input columns appear in the Model Description panel (see [Figure 6](#figure6).

## **Choosing your output column** 

The output column is the dependent variable, which represents the outcome or response that is influenced by your input variables. You can only select one output column to define the dependent variable.

**To choose your output column**

1. Select **Select Output Column**.
	The **Select Columns** dialog opens.  
3. Choose the column to be your output variable, then select Confirm Selection.   
   The Columns Selected dialog opens, stating your chosen output column.  
4. Select **OK**.   
   The selected output column appears in the Model Description panel (see Figure 6).  
   

![The information about a model that is displayed in the Model Description panel](https://imgur.com/axzztuX.png)  
<p id="figure6"><strong>Figure 6</strong>: The information about a model that is displayed in the Model Description panel<p>

# **Creating a description for your model** 

Adding a description for your model is optional, but it helps document its purpose and key characteristics, making it easier to reference later. If you choose not to add a description when creating and saving your model, Trendify will prompt you with a reminder to save a description when you click Create and Show Model. You can simply click **OK** to proceed without adding one, or you can choose to add a description at that time.

**To create a description for your model**

1. Navigate to **Model Description** (see [Figure 6](#figure6).  
2. Enter the description you want for your model.  
3. Select the **Save Description** button to store your description.  
   The **Success** dialog opens.  
4. Select **OK**.  
   Your description is saved and appears in the Model Description panel.

| Information | Explanation |
| :---- | :---- |
| Formula | The linear regression formula used by the model. |
| MSE (Mean squared error) | The average squared difference between predicted and actual values.  |
| R2 (R-Squared value) | A measure of how well the model fits the data, specifically how well the input variables explains the variability of the output variable. |
| Input Columns | The input or independent variables used in the model. |
| Output Column | The output or dependent variable used in the model. |
| File loaded | The save location or file path of the data or model you opened. |
| Result prediction | The predicted or output value of the most recent prediction you made.  |
| Description | The model description you saved. |

<p id="table4"><strong>Table 4</strong>: Explanation of information found in the Model Description panel<p>

# **Creating a model** 

Creating a model in Trendify involves selecting input and output columns to define the relationship between your dataset’s variables. Once your columns are selected, you can proceed to generate the model.

**To create a model**

1. [Choose your input columns](#choosing-your-input-columns).  
2. [Choose your output column](#choosing-your-output-column).  
3. Select **Create Model**.  
   The **Model Created** dialog opens, confirming the model has been successfully created.  
4. Select **OK**.  

# **Making predictions** 

After selecting your input and output columns and creating a model, you can use the Make a Prediction feature to calculate predicted values based on new input data. By entering a specific value for one of your input variables, Trendify will use the linear regression model to predict the corresponding output variable. This allows you to see potential outcomes based on your selected data.

**To make a prediction**

1. Select **Make Prediction** after creating your model.  
   The **Prediction** dialog opens and displays the input column you chose as the input field (see [Figure 7](#figure7).  
2. Enter a number in the input field.  
3. Select **Calculate Prediction**.  
   The predicted value appears in the “Predicted Value” field.  
4. Select the **Close** after you finish reviewing your results.  
   The predicted value is shown in the Model Description panel.

![The Prediction values dialog with population as the input column](https://imgur.com/9aFgWGA.png)
<p id="figure7"><strong>Figure 7</strong>: The <strong>Prediction values</strong> dialog with population as the input column.<p>

# **Viewing and interacting with your model graph** 

Trendify allows you to visualize the relationship between your input and output variables through a 2D linear regression or 3D multilinear regression graph (see [Figure 9](#figure9) and [Figure 10](#figure10) for examples). Viewing your model graph provides insights into how your selected variables interact. To view your model graph exactly as you need, Trendify has tools for exploring and customizing your model graph (see [Figure 8](#figure8).

**To interact with your model graph**

1. Select **Show Model** after creating your model.  
   A window with the graph of your linear regression model opens.  
2. Select any of the tool icons to interact with your model graph (see [Table 5](#table5) to learn the function of each icon).  

![The interaction tools on the linear regression model graph window](https://imgur.com/7TbtLky.png)
<p id="figure8"><strong>Figure 8</strong>: The interaction tools on the linear regression model graph window<p>

| Icon | Function |
| :---- | :---- |
| Reset original view<br>![Reset original view icon](https://imgur.com/sGshLrJ.png) | Restores your model graph to the original view settings. |
| Back to previous view<br>![Back to previous view icon](https://imgur.com/KZuqgHr.png) | Returns your model graph to your previous view setting. |
| Forward to next view<br>![Forward to next view icon](https://imgur.com/AlluxWX.png) | Goes forward in your model graph setting history, after you have selected the **Back to previous view** icon. |
| Left button pan, right button zoom<br>![Left button pan, right button zoom icon](https://imgur.com/rf2M8cC.png) | Pans when you left-click and drag over your model graph. Zooms when you right-click and drag over your model graph. |
| Zoom to rectangle<br>![Zoom to rectangle icon](https://imgur.com/bPJnNFL.png) | Zooms in to your rectangular selection. |
| Configure subplots<br>![Configure subplots icon](https://imgur.com/gCKYLuE.png) | Opens the **Subplot configuration tool** window, where you can use sliders to change the dimensions of your model graph. |
| Save the figure<br>![Save the figure icon](https://imgur.com/i9MpbSx.png) | Allows you to save an image or PDF of your model graph in its current view settings (see Saving an image or PDF of your model graph). |
<p id="table5"><strong>Table 5</strong>: The tool icons found in the model graph window and their functions<p>

![A 2D linear regression model graph, where households (output variable) is predicted based on population (input variable)](https://imgur.com/EFSYGNg.png)  
<p id="figure9"><strong>Figure 9</strong>: A 2D linear regression model graph, where households (output variable) is predicted based on population (input variable)</p>

![A 3D multiple linear regression model graph, where households (output variable) is predicted based on median housing age and population (input variables)](https://imgur.com/rjtljDJ.png)  
<p id="figure10"><strong>Figure 10</strong>: A 3D multiple linear regression model graph, where households (output variable) is predicted based on median housing age and population (input variables)</p>

## **Saving an image or PDF of your model graph**

You can use Trendify to directly save an image or PDF of your model graph to your device. Trendify offers a variety of file formats to save your model graph in, such as:

* Raster images  
  * Portable Network Graphics (PNG)  
  * Joint Photographic Experts Group (JPEG or JPG)  
  * Raw RGBA Bitmap (RGBA)  
* Vector images  
  * Encapsulated PostScript (EPS)  
  * Scalable Vector Graphics (SVG)  
  * PostScript (PS)  
* Portable Document Format (PDF)

**To save an image or PDF of your model graph**

1. Select **Show Model** after creating your model.  
   A window with the graph of your linear regression model opens.  
2. Select the **Save the figure** icon.  
   The **Save the figure** dialog opens.  
3. Navigate to the folder you want to save your image or PDF to.  
4. Enter the name you want to give your image or PDF.  
5. Choose the file type you want to save your image or PDF as.  
   Your model graph image or PDF is saved to your device.

# **Saving Your Model** 

Saving your model in Trendify ensures you can reuse it later without needing to recreate it. These models can also be reloaded into Trendify for future analysis. 

**To save your model**

1. Select **Save Model**.  
   The **Save as** dialog will appear.  
2. Enter the name you want to give your model.  
3. Choose to save your model as a pkl or joblib file type.  
4. Select **Save**.  
   The **Model Saved** dialog is opened and states the file path where your model is saved.

Refer to the [Loading an existing model on Trendify](#loading-an-existing-model-on-trendify) section to learn how to reuse saved models in Trendify.

# **Glossary** 

**Constant**

A fixed value that does not change.

**Categorical data**

Data that represents categories or groups, such as:

* Blonde, brown, red, and black  
* Yes or no

It is often non-numerical, but can be represented by a number, for example:

* Yes = 0  
* No = 1

**Dependent variable**

The output variable you want to predict or explain in a model. It depends on the values of the independent variables. In Trendify, the dependent variable is the output column. 

**Independent variable**

The input variables that are used to predict or explain the dependent variable. In Trendify, the independent variables are the input columns.

**Linear regression** 

Also known as simple linear regression. A model that represents the relationship between one independent variable and one dependent variable with a straight line of best fit. Linear regression models are used to make predictions or analyze trends.

**Mean**

The average of a set of numbers that is calculated by adding up all the values and dividing by the total number of values.

**Mean squared error (MSE)**

A measure of how far the predicted values are from the actual values in a model. It calculates the average of the squared differences between them. Lower values mean the model is more accurate.

**Median**

The middle value in a sorted list of numbers, where half of the values are above and half are below it.

**Model**

A mathematical or computational representation of a process or system that is used to make predictions based on input data. In machine learning, a model is created using algorithms that learn patterns from data to make future predictions.

**Multiple linear regression**

A statistical method used to model the relationship between a dependent variable and two or more independent variables by fitting a linear equation to observed data.

**Null values**

Data points that are missing or undefined within a dataset, often represented as "nan" (not a number) or blanks.

**Numerical data**

Data that represents quantities and can be measured on a numerical scale, such as age, income, or temperature.

**Preprocess** 

The process of cleaning, transforming, and organizing raw data into a format suitable for analysis or modeling, often including handling missing values, scaling, and encoding.

**R-squared value**

A statistical measure that indicates how well the independent variables explain the variability of the dependent variable, also known as the coefficient of determination. It ranges from 0 to 1, with the model fitting that data better the closer the measure is to 1.
