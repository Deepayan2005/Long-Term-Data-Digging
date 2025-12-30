import io,pathlib,matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plotter
from fpdf import FPDF


class DataReportMaker:
    
    def __init__(self,name:str,data,folder:pathlib.Path):
        self.name=name
        self.details=data
        self.folder=folder
        self.pdf = FPDF(format='A4',orientation='L')
        self.images_per_page = 0
        self.pdf.add_page()


    def save_file(self):
        path = f"{self.folder}/{self.name}.pdf"
        self.pdf.output(path)
        print(f"Report for {self.name} saved...")


    def put_graph_image(self,plot_name:str,x_label:str,y_label:str,x_axis:str,y_axis:str,
                        graph_type:str,coordinate:tuple[int,int],colors=False):
        '''

        :param plot_name: title of the graph
        :param x_label: X-Label
        :param y_label: Y-Label
        :param x_axis: key for data in X-axis
        :param y_axis: key for data in Y-axis
        :param graph_type: line graph / bar graph
        :param coordinate: [int,int] coordinates for placing the image
        :param colors: want to show colors or not
        :return: returns nothing
        '''

        if self.images_per_page%4==0 and self.images_per_page>0:
            self.pdf.add_page()

        if graph_type.lower()=='line':
            buf=io.BytesIO()

            plotter.xlabel(x_label)
            plotter.ylabel(y_label)
            plotter.plot(self.details[x_axis], self.details[y_axis])
            plotter.title(plot_name)
            plotter.tight_layout()
            plotter.savefig(buf,bbox_inches="tight")
            plotter.close()
            buf.seek(0)

            self.pdf.image(buf, x=coordinate[0], y=coordinate[1], w=130, keep_aspect_ratio=True)
            buf.flush()
            buf.close()
            self.images_per_page+=1

        elif graph_type.lower()=='bar':
            buf=io.BytesIO()

            plotter.xlabel(x_label)
            plotter.ylabel(y_label)

            shown_colors = []
            if colors:
                for i in self.details[y_axis]:
                    if i<0:shown_colors.append('red')
                    else:shown_colors.append('green')
                plotter.bar(self.details[x_axis], self.details[y_axis],color=shown_colors)
            else:
                plotter.bar(self.details[x_axis], self.details[y_axis])

            plotter.title(plot_name)
            plotter.tight_layout()

            plotter.savefig(buf,bbox_inches="tight")
            plotter.close()
            buf.seek(0)

            self.pdf.image(buf, x=coordinate[0], y=coordinate[1], w=130, keep_aspect_ratio=True)
            buf.flush()
            buf.close()
            self.images_per_page+=1

            
        
        
    
    
    