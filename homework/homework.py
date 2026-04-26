"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel
import zipfile
import pandas as pd
import os


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    def csv(df,output_path, name):
        df.to_csv(output_path + '/'+name+'.csv',index=False)

    input_path = "files/input"
    output_path = "files/output"
    dfs = []
    for zip_folder in os.listdir(input_path):
        zip_folder_path = os.path.join(input_path,zip_folder)
        with zipfile.ZipFile(zip_folder_path,'r') as z:
            files = z.namelist()
            for file in files:
                if not file.endswith('.csv'):
                    continue
                with z.open(file) as f:
                    df = pd.read_csv(f)
                    dfs.append(df)
    
    df = pd.concat(dfs, ignore_index=True)

    # client
    client = df.copy()[['client_id','age','job','marital','education','credit_default','mortgage']]

    client['job'] = client['job'].str.replace('.','').str.replace('-','_')
    client['education'] = client['education'].str.replace('.','_')
    client['education'] = client['education'].replace('unknown',pd.NA)
    client['credit_default'] = (client['credit_default'] == 'yes').astype(int)
    client['mortgage'] = (client['mortgage'] == 'yes').astype(int)

    csv(df=client,output_path=output_path,name='client')

    # campaign
    campaign =  df.copy()[['client_id','number_contacts','contact_duration','previous_campaign_contacts','previous_outcome','campaign_outcome','day','month']]

    campaign['previous_outcome'] = (campaign['previous_outcome'] == 'success').astype(int)
    campaign['campaign_outcome'] = (campaign['campaign_outcome'] == 'yes').astype(int)
    campaign['month'] = campaign['month'].str.capitalize()
    campaign['month'] = pd.to_datetime(campaign['month'], format='%b').dt.month.astype(str).str.zfill(2)
    campaign['day'] = campaign['day'].astype(str).str.zfill(2)
    campaign['last_contact_date'] = '2022-' + campaign['month'].astype(str) + '-' + campaign['day'].astype(str)
    campaign = campaign.drop(columns=['day','month'])

    csv(df=campaign,output_path=output_path,name='campaign')

    # economics
    economics = df.copy()[['client_id','cons_price_idx','euribor_three_months']]
    csv(df=economics,output_path=output_path,name='economics')


    return 


if __name__ == "__main__":
    clean_campaign_data()
