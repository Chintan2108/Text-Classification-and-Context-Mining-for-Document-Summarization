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
        sentencemodel.categorizer()

sm = SimilarityMapping('Responses_All About the RMP2031.xlsx')
sm.driver()