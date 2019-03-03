import pandas as pd
import csvparser, sentencemodel

class SimilarityMapping:
    '''
    This class consumes the model and sequences the flow of execution for the given input
    '''
    def __init__(self, path):
        self.filepath = path

    def driver(self):

        #parsing the input file for having sampled input to the model
        csvparser.parse(self.filepath)
        results = sentencemodel.categorizer()

        downloadOutput = pd.ExcelWriter('results.xlsx', engine='xlsxwriter')

        for domain in results:
            print('Writing Excel for domain %s' % domain)
            df = pd.DataFrame({ key:pd.Series(value) for key, value in results[domain].items() })
            df.to_excel(downloadOutput, sheet_name=domain)
        downloadOutput.save()
sm = SimilarityMapping('Responses_All About the RMP2031.xlsx')
sm.driver()