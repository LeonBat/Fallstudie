#Libraries
import pandas as pd


#This script transforms metadata csv files in tsv files



#transformer function
def metadata_transformer(input_csv:pd.DataFrame, output_tsv: str) -> None:
    '''
    The function takes a pandas dataframe as input and saves it as a tsv file
        Parameters:
        ----------
        input_csv : pd.DataFrame
            Input metadata in csv format as pandas dataframe
        output_tsv : str
            File path to save the transformed metadata in tsv format
    '''
    input_csv.to_csv(output_tsv, sep = '\t', index = False)


#Execution
if __name__ == "__main__":
    #Input metadata csv file path
    input_csv_fp = 'Data/metadata_for_q.csv'
    
    #Output metadata tsv file path
    output_tsv_fp = 'Data/metadata.tsv'
    
    #Read the input csv file as pandas dataframe
    input_csv_df = pd.read_csv(input_csv_fp, sep = ";")
    
    #Call the transformer function
    metadata_transformer(input_csv_df, output_tsv_fp)