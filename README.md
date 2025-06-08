# 🎓 EDU Sentiment Analysis Pipeline

A full-stack sentiment analysis and keyword extraction system tailored for analyzing student feedback from educational institutions. The pipeline supports data ingestion from MySQL, preprocessing, NLP sentiment modeling, keyword analysis, result storage, and interactive visualization via Streamlit.

---

## 📁 Project Structure

```
EDUSENTIMENT/
├── analysis/
│   ├── accuracy.py
│   └── sentiment.py
├── data/
│   ├── departments.csv
│   ├── feedback.csv
│   ├── predictions.csv
│   ├── student_labelled_data.csv
│   └── students.csv
├── database/
│   ├── database_input.py
│   └── database_output.py
├── nlp/
│   ├── keyword_extraction.py
│   ├── preprocess.py
│   ├── text_cleaning.py
│   └── text_tokenize.py
├── venv/                          # Virtual environment (optional to track in Git)
├── .env
├── .gitignore
├── dashboard.py
├── main.py
├── query.sql
└── requirements.txt

````

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/edusentiment.git
cd edusentiment
````

### 2. Create a Virtual Environment and Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Prepare `.env` File

Create a `.env` file with the following keys:

```ini
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=edusentiment
```

### 4. Ensure Required NLTK Downloads

```python
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
```

---

## 🧠 What It Does

### 🔄 `main.py`

* Connects to MySQL using `database_input.py`
* Preprocesses feedback text
* Performs sentiment classification using `cardiffnlp/twitter-roberta-base-sentiment`
* Extracts keywords via `YAKE`
* Saves results to the database and a predictions CSV
* Evaluates prediction accuracy against labeled data

### 📊 `dashboard.py`

* Interactive **Streamlit dashboard**:

  * Department filtering
  * Sentiment distribution over time
  * Keyword visualization by sentiment
  * Feedback-level drill-down

---

## 💡 Key Modules

| Module                  | Purpose                                                |
| ----------------------- | ------------------------------------------------------ |
| `database_input.py`     | Loads raw feedback from MySQL                          |
| `database_output.py`    | Saves processed results to MySQL                       |
| `preprocess.py`         | Cleans and normalizes feedback text                    |
| `sentiment.py`          | Applies RoBERTa-based sentiment analysis               |
| `keyword_extraction.py` | Extracts meaningful keywords                           |
| `accuracy.py`           | Compares predicted vs. actual sentiment for evaluation |
| `dashboard.py`          | Streamlit UI for monitoring feedback insights          |

---

## 🚀 To Run the App

### Run the Pipeline

```bash
python main.py
```

### Launch the Dashboard

```bash
streamlit run dashboard.py
```

---

## ✅ Features

* Pretrained RoBERTa sentiment model
* Custom preprocessing pipeline for educational feedback
* Robust keyword filtering
* Auto-saving to MySQL with JSON serialization for complex columns
* Responsive and insightful dashboard

---

## 🗄️ MySQL Database Setup

```sql
-- Create the database
CREATE DATABASE edusentiment;

-- Use the database
USE edusentiment;

-- Create the students table
CREATE TABLE students (
    student_id VARCHAR(10) PRIMARY KEY,
    student_name VARCHAR(100),
    email VARCHAR(100),
    enrollment_year INT
);

-- Create the departments table
CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100)
);

-- Create the feedback table
CREATE TABLE feedback (
    feedback_id INT PRIMARY KEY,
    student_id VARCHAR(10),
    department_id INT,
    date DATE,
    feedback_text TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

Load the csv files into respective tables using mysql workbench import wizard option.

-- Create an enriched feedback view
CREATE TABLE feedback_enriched AS
SELECT 
    f.feedback_id,
    d.department_name,
    f.student_id,
    f.date,
    f.feedback_text
FROM feedback f
JOIN departments d ON f.department_id = d.department_id
JOIN students s ON f.student_id = s.student_id;

-- View the enriched data
SELECT * FROM feedback_enriched;
```

---

## 📌 Notes

* The model limits text input to 512 characters (RoBERTa limitation).
* Ensure `student_labelled_data.csv` is present in the `data/` folder for evaluation.
* Keywords are extracted per `(department, sentiment)` combination.

---

## 📬 Contact

Maintained by [Md Nasir](mailto:mdnasir020396@gmail.com)
Feel free to contribute or raise issues!
