import matplotlib.pyplot as plt
import warnings
import numpy as np

class MatLib:

    def __init__(self, info):
        warnings.filterwarnings("ignore")
        self.info=info

        print(self.info)

        self.pie_chart()
        self.bar_chart_comment()


    #comment_karma, link_karma
    def pie_chart(self):

        labels = 'Link Karma', 'Comment Karma'
        sizes = [self.info['link_karma'], self.info['comment_karma']]
        colors = ['red', 'green']
        explode = (0, 0) # only "explode" the 2nd slice (i.e. 'Hogs')

        plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=90)
        # Set aspect ratio to be equal so that pie is drawn as a circle.
        plt.axis('equal')

        plt.show()


    #favorite_words_comment
    #info['favorite_words_comment'] = 
    #info['favorite_words_title'] =
    def bar_chart_comment(self):

        values = []
        keys = []

        for word in self.info['favorite_words_comment']:
            keys.append(word[0])
            values.append(word[1])
        

        n_groups = 10

        fig, ax = plt.subplots()

        index = np.arange(n_groups)

        bar_width = 0.45

        opacity = 0.5
        error_config = {'ecolor':'0.3'}

        rect1 = plt.bar(index, values, bar_width,
                        alpha=opacity,
                        color='b',
                        error_kw=error_config,
                        label=None)

        plt.xlabel('Words')
        plt.ylabel('Number of Times Used')
        plt.xticks(index , keys)
        plt.legend()

        plt.tight_layout()
        plt.show()
            

    def bar_chart_title(self):
        dd = 4
            
