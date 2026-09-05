# ==========================================
# EMPLOYEE DATA CLEANING & QUALITY VALIDATION
# ==========================================

import pandas as pd


def clean_employee_data(df):

    # ==========================================
    # 1. CREATE COPY
    # ==========================================

    df = df.copy()


    # ==========================================
    # 2. CLEAN TEXT COLUMNS
    # ==========================================

    text_columns = [

        "employee_code",
        "first_name",
        "last_name",
        "employee_name",
        "gender",
        "email",
        "phone",
        "department_name",
        "role_name",
        "location_name",
        "city",
        "employee_status"

    ]


    for column in text_columns:

        if column in df.columns:

            df[column] = (

                df[column]

                .astype("string")

                .str.strip()

            )


    # ==========================================
    # 3. CONVERT NUMERIC COLUMNS
    # ==========================================

    numeric_columns = [

        "employee_id",
        "experience_years",
        "basic_salary"

    ]


    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(

                df[column],

                errors="coerce"

            )


    # ==========================================
    # 4. CONVERT DATE COLUMNS
    # ==========================================

    date_columns = [

        "date_of_birth",
        "hire_date"

    ]


    for column in date_columns:

        if column in df.columns:

            df[column] = pd.to_datetime(

                df[column],

                errors="coerce"

            )


    # ==========================================
    # 5. REMOVE DUPLICATE EMPLOYEES
    # ==========================================

    if "employee_id" in df.columns:

        df = df.drop_duplicates(

            subset=["employee_id"]

        )


    # ==========================================
    # 6. DATA QUALITY VALIDATION
    # ==========================================

    invalid_records = pd.Series(

        False,

        index=df.index

    )


    # Employee ID must exist

    if "employee_id" in df.columns:

        invalid_records |= (

            df["employee_id"].isna()

        )


    # Employee code must exist

    if "employee_code" in df.columns:

        invalid_records |= (

            df["employee_code"].isna()

            |

            (df["employee_code"] == "")

        )


    # First name must exist

    if "first_name" in df.columns:

        invalid_records |= (

            df["first_name"].isna()

            |

            (df["first_name"] == "")

        )


    # Last name must exist

    if "last_name" in df.columns:

        invalid_records |= (

            df["last_name"].isna()

            |

            (df["last_name"] == "")

        )


    # Email must exist and contain @

    if "email" in df.columns:

        invalid_records |= (

            df["email"].isna()

            |

            ~df["email"].str.contains(

                "@",

                na=False

            )

        )


    # Experience cannot be negative

    if "experience_years" in df.columns:

        invalid_records |= (

            df["experience_years"] < 0

        )


    # Salary cannot be negative

    if "basic_salary" in df.columns:

        invalid_records |= (

            df["basic_salary"] < 0

        )


    # ==========================================
    # 7. REMOVE INVALID RECORDS
    # ==========================================

    df = df[

        ~invalid_records

    ]


    # ==========================================
    # 8. RESET INDEX
    # ==========================================

    df = df.reset_index(

        drop=True

    )


    return df