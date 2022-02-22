#The purpose of this script was to iterate through several mxds and update the logos on the map with a new jpeg. Additionally, the text element that states
#when the map was last updated is fixed to show the current time and day

import os
import arcpy
import datetime

class Wood_Cutting_Maps:
	def __init__(self, input_file_or_folder, output_folder):
		self.input_file_or_folder = input_file_or_folder
		self.output_folder = output_folder

	def env_workspace(self):
		self.input_file_or_folder = r"C:\Users\ahimmelberger\Desktop\Projects\Recreation\Wood Cutting\2. MXDs"
		self.output_folder = r"C:\Users\ahimmelberger\Desktop\Projects\Recreation\Wood Cutting\4. PDFs"
		for root, dirs, files in os.walk(self.input_file_or_folder):
			for f in files:
				if f.endswith(".mxd"):
					maps = root + "\\" + f

					current_day = datetime.date.today()
					formatted_date = datetime.date.strftime(current_day, "%m/%d/%Y")
					year = datetime.date.strftime(current_day, "%Y")
					mxd = arcpy.mapping.MapDocument(maps)
					
					for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
						if elm.name == "Last_Updated":
							elm.text = str("Last Updated: ") + formatted_date
						if elm.name == "Title":
							elm.text = str(year) + str(" WOOD \nCUTTING MAP ")


					for logo in arcpy.mapping.ListLayoutElements(mxd, "PICTURE_ELEMENT"):
						if logo.name == "FWA_Insignia_242":
							logo.sourceImage = r"C:\Users\ahimmelberger\Desktop\GIS\Templates\FWA_Insignia_gray.jpg"
						if logo.name == "amc-shield":
							logo.sourceImage = r"C:\Users\ahimmelberger\Desktop\GIS\Templates\amc_shield_gray.jpg"
						if logo.name == "SCAREBEAR_Transparent":
							logo.sourceImage = r"C:\Users\ahimmelberger\Desktop\GIS\Templates\SCAREBEAR_gray.jpg"

					output_name = f.split(".")[0]
					output_path =  self.output_folder + "\\" + output_name + ".pdf"
					print output_path
					#folder with name with extensions. Look at maps variable for clues
					arcpy.mapping.ExportToPDF(mxd, output_path, resolution = 500)
					mxd.save()


if __name__ == "__main__":
	input_file_or_folder = arcpy.GetParameterAsText(0)
	output_folder = arcpy.GetParameterAsText(1)
	pdf = Wood_Cutting_Maps(input_file_or_folder, output_folder)
	pdf.env_workspace()
