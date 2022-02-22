import os
import arcpy


class Rec_Map_Layers_to_GDB:
	def __init__(self, folder_path, input_gdb):
		self.folder_path = folder_path
		self.Rec_map_gdb = Rec_map_gdb


	def put_layers_into_gdb(self):
		arcpy.env.workspace = r"F:\Anthony\Projects\Recreation\Kiosk Maps\2. MXDs\Test"
		count = 0
		for root, dirs, files in os.walk(self.folder_path):
			for f in files:
				if f.endswith(".mxd"):
					maps = root + "\\" + f
					mxd = arcpy.mapping.MapDocument(maps)
					dataframe = arcpy.mapping.ListDataFrames(mxd)
					print dataframe
					for df in dataframe:
						feature_classes = arcpy.mapping.ListLayers(mxd, "", df)
						# print feature_classes
						print feature_classes
						for layer in arcpy.mapping.ListLayers(mxd, "", df):
							old_source = layer.dataSource
							print "Old source is: " + old_source
							source_name = layer.datasetName
							print "source name is : " + source_name
							new_source = self.Rec_map_gdb + "\\"+ source_name
							print "New source will be: " +  new_source
							if arcpy.Exists(new_source):
								pass
							elif source_name == "FWA_HILLSHADE":
								pass
							elif source_name == "DTA_HILLSHADE":
								pass
							else:
								arcpy.management.CopyFeatures(old_source, new_source) 



if __name__ == "__main__":
	folder_path = r"F:\Anthony\Projects\Recreation\Kiosk Maps\2. MXDs\Test"
	Rec_map_gdb = r"F:\Anthony\Projects\Recreation\Kiosk Maps\2. MXDs\Test\Rec_Map_DTA.gdb"
	#mxd_folder = r"F:\Anthony\Projects\Recreation\Moose Maps\2. MXDs\Final_Maps\NEW"
	find_fix = Rec_Map_Layers_to_GDB(folder_path, Rec_map_gdb)
	# find_fix.unique_layers_list()
	find_fix.put_layers_into_gdb()