import pandas as pd

def transform_dim_employee(
    df_employee: pd.DataFrame,
    df_person: pd.DataFrame,
    df_sales_person: pd.DataFrame
) -> pd.DataFrame:
    """
    Transforma DimEmployee. Granularidad: una fila por empleado.
    """
    # Empleado + nombre (Person.Person tiene los nombres con el mismo BusinessEntityID)
    df = df_employee.merge(
        df_person[['BusinessEntityID', 'FirstName', 'MiddleName', 'LastName', 'NameStyle']],
        on='BusinessEntityID', how='left')

    # Si el empleado está en la tabla de vendedores, es vendedor y tiene territorio
    df = df.merge(df_sales_person[['BusinessEntityID', 'TerritoryID']],
                  on='BusinessEntityID', how='left')
    df['SalesPersonFlag'] = df['BusinessEntityID'].isin(df_sales_person['BusinessEntityID'])
    df['SalesTerritoryKey'] = df['TerritoryID']

    # Llaves y columnas con nombre distinto al de origen
    df['EmployeeKey'] = df['BusinessEntityID']
    df['EmployeeNationalIDAlternateKey'] = df['NationalIDNumber']
    df['Title'] = df['JobTitle']  # en la DW, Title guarda el cargo

    # Columnas que no traemos de la base de origen: quedan vacías (NULL)
    df['ParentEmployeeKey'] = None
    df['EmailAddress'] = None
    df['Phone'] = None
    df['EmergencyContactName'] = None
    df['EmergencyContactPhone'] = None
    df['PayFrequency'] = None
    df['BaseRate'] = None
    df['DepartmentName'] = None
    df['StartDate'] = None
    df['EndDate'] = None
    df['Status'] = None

    # Columnas en el orden de DimEmployee del DDL (29 columnas)
    cols = [
        'EmployeeKey', 'ParentEmployeeKey', 'EmployeeNationalIDAlternateKey', 'SalesTerritoryKey',
        'FirstName', 'LastName', 'MiddleName', 'NameStyle', 'Title', 'HireDate', 'BirthDate',
        'LoginID', 'EmailAddress', 'Phone', 'MaritalStatus', 'EmergencyContactName',
        'EmergencyContactPhone', 'SalariedFlag', 'Gender', 'PayFrequency', 'BaseRate',
        'VacationHours', 'SickLeaveHours', 'CurrentFlag', 'SalesPersonFlag',
        'DepartmentName', 'StartDate', 'EndDate', 'Status'
    ]
    return df[cols]