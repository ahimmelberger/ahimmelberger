import os
import arcpy
arcpy.env.overwriteOutput = True

class FindFix_MXDs:
	def __init__(self, folder_path, input_gdb):
		self.folder_path = folder_path
		self.input_gdb = input_gdb

	def feature_list(self):
		self.sdsfie_fcs = {u'TrappingLocation_L': u'Natural_Resources', u'EncroachmentPriorityArea_A': u'Environmental_Common_and_Cross_Functional', u'HistoricRiverAlignment_L': u'Natural_Resources', u'RailroadYard_A': u'CCF_Transportation', u'GasUtilitySegment_L': u'PW_Gas', u'PestManagement_A': u'Natural_Resources', u'RegulatedAirspace': u'Airfield', u'FiringSite_P': u'Military_Ranges_and_Training', u'ElectricalUtilityNode_Xformer_P': u'PW_Electrical', u'PotentialContaminationSite_A': u'Compliance', u'ElectricalUtilityNode_P': u'PW_Electrical', u'Grid_A': u'Military_Ranges_and_Training', u'RangeLimitMarker': u'Military_Ranges_and_Training', u'MilitaryObservationPosition_A': u'Military_Ranges_and_Training', u'PestManagement_P': u'Natural_Resources', u'HazardousMaterialManagement_Tk_P': u'Compliance', u'ObservationLookout_P': u'Recreation', u'WaterUtilityNode_Hydrant_P': u'PW_Water', u'ThermalUtilitySegment_L': u'PW_Thermal', u'EnvironmentalDischarge_P': u'Compliance', u'NonDodPropertyOfConcern_A': u'Environmental_Common_and_Cross_Functional', u'ElectricalUtilityNode_ArfldLgt_P': u'PW_Electrical', u'PavementSection_Airfield_A': u'CCF_Transportation', u'SpecialUseAirspace': u'Airfield', u'MilitaryRangeBerm_A': u'Military_Ranges_and_Training', u'GolfCourse_A': u'Recreation', u'ElectricalUtilityNode_Meter_P': u'PW_Electrical', u'HistoricStructureSite_A': u'Cultural_Resources', u'UtilityFeature_WWJunction_P': u'PW_Waste_Water', u'RecreationTrail_L': u'Recreation', u'UtilityFeature_PolManhole_P': u'PW_POL', u'WastewaterUtilityNode_Area_A': u'PW_Waste_Water', u'LandManagementZone_A': u'Planning', u'Tower_P': u'Real_Property', u'ElectricalUtilityNode_Substatn_P': u'PW_Electrical', u'CulturalResourcePotential_A': u'Cultural_Resources', u'HabitatProtectiveZone_Fauna_A': u'Natural_Resources', u'Wall_L': u'Common_and_Cross_Functional', u'Cemetery_P': u'Cemetery_Operations', u'ElectricalUtilityNode_Generatr_P': u'PW_Electrical', u'Dam_A': u'Civil_Works', u'HistoricLandscape_A': u'Cultural_Resources', u'WaterUtilityNode_Pump_P': u'PW_Water', u'ForwardArmingRefueling_P': u'Military_Ranges_and_Training', u'WaterUtilityNode_Tank_P': u'PW_Water', u'RoadCenterline_L': u'CCF_Transportation', u'Cemetery_A': u'Cemetery_Operations', u'RailSegment_L': u'CCF_Transportation', u'ContaminationSite_A': u'Clean_Up', u'RecreationBoundary_A': u'Recreation', u'ForwardArmingRefueling_A': u'Military_Ranges_and_Training', u'ThermalUtilityNode_P': u'PW_Thermal', u'Structure_Storage_A': u'Real_Property', u'RangeEntrance': u'Military_Ranges_and_Training', u'LramSite_P': u'Military_Ranges_and_Training', u'MilitaryTarget_L': u'Military_Ranges_and_Training', u'AccessControl_Barricade_P': u'Real_Property', u'MilitaryTarget_A': u'Military_Ranges_and_Training', u'PavementMarking_A': u'CCF_Transportation', u'LramSite_A': u'Military_Ranges_and_Training', u'AquiferRecharge_A': u'Natural_Resources', u'MilitaryTarget_P': u'Military_Ranges_and_Training', u'Wetland_A': u'Natural_Resources', u'LramSite_L': u'Military_Ranges_and_Training', u'AdministrativeBoundary_A': u'Common_and_Cross_Functional', u'WastewaterUtilityNode_Valve_P': u'PW_Waste_Water', u'ImpactArea': u'Military_Ranges_and_Training', u'PolUtilitySegment_L': u'PW_POL', u'ArtifactFeaturePoint_P': u'Cultural_Resources', u'Incident_P': u'Emergency_Services', u'ElevationContour_L_Out': u'Common_and_Cross_Functional', u'LandParcel_A': u'Real_Property', u'WildlandFire_A': u'Emergency_Services', u'ArchaeologicalSite_P': u'Cultural_Resources', u'WastewaterUtilityNode_P': u'PW_Waste_Water', u'PavementSection_Sidewalk_A': u'CCF_Transportation', u'ParkingArea_A': u'CCF_Transportation', u'GroundsMaintenance_A': u'Common_and_Cross_Functional', u'StormwaterUtilitySegment_Clvrt_L': u'PW_Stormwater', u'LandUse_A': u'Planning', u'Structure_MntAndOper_A': u'Real_Property', u'HistoricObject_P': u'Cultural_Resources', u'MilitaryTrainingLocation_TrngA': u'Military_Ranges_and_Training', u'RadarEquipment_P': u'PW_Communications', u'StormwaterUtilitySegment_OpnDn_L': u'PW_Stormwater', u'ElectricalUtilityNode_Switch_P': u'PW_Electrical', u'RtlaSite_P': u'Military_Ranges_and_Training', u'StormwaterUtilityNode_Dischrge_P': u'PW_Stormwater', u'Structure_A': u'Real_Property', u'Grid_L': u'Military_Ranges_and_Training', u'WaterUtilityNode_Valve_P': u'PW_Water', u'FutureProjectSite_A': u'Planning', u'MilitaryRange_A': u'Military_Ranges_and_Training', u'Firebreaks_L': u'Emergency_Services', u'AirfieldImaginarySurface_A': u'Airfield', u'RecreationFeature_Campground_A': u'Recreation', u'RtlaSite_A': u'Military_Ranges_and_Training', u'Structure_P': u'Real_Property', u'SpecialStatusSpecies_Fauna_P': u'Natural_Resources', u'FutureProjectSite_P': u'Planning', u'RtlaSite_L': u'Military_Ranges_and_Training', u'ElevationContour_L': u'Common_and_Cross_Functional', u'SupportStructure_UtilityPole_P': u'PW_Other', u'RecreationFeature_Campsite_A': u'Recreation', u'ForestTimberHarvest_A': u'Natural_Resources', u'UxoContamination_P': u'Clean_Up', u'HistoricDistrict_A': u'Cultural_Resources', u'StormwaterUtilityNode_Inlet_P': u'PW_Stormwater', u'Structure_Pad_A': u'Real_Property', u'SpotElevation_P': u'Common_and_Cross_Functional', u'UxoContamination_A': u'Clean_Up', u'NuisanceSpecies_P': u'Natural_Resources', u'RecreationFeature_A': u'Recreation', u'Installation_A': u'Real_Property', u'WastewaterUtilitySegment_L': u'PW_Waste_Water', u'ForestInventory_A': u'Natural_Resources', u'Building_A': u'Real_Property', u'AmmunitionStorage_A': u'Military_Ranges_and_Training', u'CommUtilityNode_Antenna_P': u'PW_Communications', u'SoilMapUnit_A': u'Natural_Resources', u'WaterUtilityNode_Fitting_P': u'PW_Water', u'FishingLocation_A': u'Recreation', u'MilitaryTrainingLocation_Ste_P': u'Military_Ranges_and_Training', u'PitOrQuarry_P': u'Common_and_Cross_Functional', u'MilitaryLandingZone_A': u'Military_Ranges_and_Training', u'Inundation_A': u'Civil_Works', u'EsqdArc': u'Military_Ranges_and_Training', u'GolfCourseFeature_A': u'Recreation', u'MilitaryTrainingLocation_Ste_L': u'Military_Ranges_and_Training', u'FishingLocation_P': u'Recreation', u'MilitaryTrainingLocation_Ste_A': u'Military_Ranges_and_Training', u'MilitaryLandingZone_P': u'Military_Ranges_and_Training', u'PitOrQuarry_A': u'Common_and_Cross_Functional', u'MilitaryTrainingLocation_TrngAAnno': u'Military_Ranges_and_Training', u'RangeControllerPosition': u'Military_Ranges_and_Training', u'MilitaryRangeEquipment': u'Military_Ranges_and_Training', u'SurfaceDangerZone_A': u'Military_Ranges_and_Training', u'SolidWasteLandfill_A': u'Real_Property', u'Sign_P': u'Common_and_Cross_Functional', u'AdminBoundary_Fire_A': u'Emergency_Services', u'NoiseZone_A': u'Environmental_Common_and_Cross_Functional', u'WaterFeature_L': u'Natural_Resources', u'CulturalSurvey_A': u'Cultural_Resources', u'WaterFeature_A': u'Natural_Resources', u'StormwaterUtilitySegment_L': u'PW_Stormwater', u'PolUtilityNode_Tank_P': u'PW_POL', u'HazardousWasteManagement_A': u'Compliance', u'CommUtilitySegment_L': u'PW_Communications', u'MilitaryLocalFlyingArea': u'Airfield', u'Vegetation_A_Out': u'Natural_Resources', u'WaterUtilitySegment_L': u'PW_Water', u'Wetland_A_Out': u'Natural_Resources', u'Structure_Canopy_A': u'Real_Property', u'Tree_P': u'Natural_Resources', u'WaterFeature_A_Labels_Big_RiversAnno': u'Natural_Resources', u'WaterUtilityNode_TreatmentPlnt_P': u'PW_Water', u'AdminBoundary_Police_A': u'Emergency_Services', u'EnvironmentalSample_P': u'Compliance', u'FutureProjectBoundary_A': u'Planning', u'FiringSite_A': u'Military_Ranges_and_Training', u'UtilityFeature_SWJunction_P': u'PW_Stormwater', u'FiringSite_L': u'Military_Ranges_and_Training', u'UnexplodedOrdnanceClearance_A': u'Clean_Up', u'WaterUtilityNode_Meter_P': u'PW_Water', u'MilitaryObservationPosition_P': u'Military_Ranges_and_Training', u'RestrictedArea_MilitaryRange_A': u'Military_Ranges_and_Training', u'Outgrant_A': u'Real_Property', u'WatershedFeature_A': u'Natural_Resources', u'MilitaryRangeBerm_L': u'Military_Ranges_and_Training', u'Site_A': u'Real_Property', u'ElectricalUtilitySegment_L': u'PW_Electrical', u'MilitaryDropZone_A': u'Military_Ranges_and_Training', u'AerialObstruction': u'Airfield', u'Bridge_A': u'CCF_Transportation', u'Bridge_L': u'CCF_Transportation', u'WastewaterUtilityNode_Fitting_P': u'PW_Waste_Water', u'PavementSection_Roadway_A': u'CCF_Transportation', u'LandCover_A': u'Common_and_Cross_Functional', u'GasUtilityNode_P': u'PW_Gas', u'UtilityFeature_ElecJunction_P': u'PW_Electrical', u'Well_P': u'Environmental_Common_and_Cross_Functional', u'RecreationFeature_Playground_A': u'Recreation', u'AmmunitionStorage_P': u'Military_Ranges_and_Training', u'SpeciesStudySite_Fauna_P': u'Natural_Resources', u'AirAccidentPotentialZone_A': u'Airfield', u'AccessControl_P': u'Real_Property', u'Vegetation_A': u'Natural_Resources', u'EnvironmentalRestorationSite_A': u'Clean_Up', u'ControlMonument_P': u'Civil_Works', u'ElectricalUtilityNode_ExterLgt_P': u'PW_Electrical', u'HuntingLocation_A': u'Recreation', u'Grid_P': u'Military_Ranges_and_Training', u'Fence_L': u'Common_and_Cross_Functional', u'MilitaryTrainingLocation_Trng_L': u'Military_Ranges_and_Training', u'SpeciesLocation_Fauna_P': u'Natural_Resources', u'HuntingLocation_P': u'Recreation', u'CommUtilityNode_Speaker_P': u'PW_Communications', u'MilitaryTrainingRoute': u'Airfield', u'PavementSection_A': u'CCF_Transportation', u'SupportStructure_L': u'PW_Other'}
		
		self.general_layers_gdb = r"F:\Anthony\Projects\Recreation\iSportsman Documentation\1. GIS data\General_Layers.gdb"
		self.general_layers_list = []
		arcpy.env.workspace = self.general_layers_gdb
		for dataset in arcpy.ListDatasets():
			for fc in arcpy.ListFeatureClasses("*", "ALL", dataset):
				fcList.append(fc)
		for fc in arcpy.ListFeatureClasses():
			self.general_layers_list.append(fc)
		print self.general_layers_list

		self.kiosk_maps_gdb = r"F:\Anthony\Projects\Recreation\Kiosk Maps\1. GIS data\Kiosk_Maps.gdb"
		self.kiosk_maps_list = []
		arcpy.env.workspace = self.kiosk_maps_gdb
		for dataset in arcpy.ListDatasets():
			for fc in arcpy.ListFeatureClasses("*", "ALL", dataset):
				fcList.append(fc)
		for fc in arcpy.ListFeatureClasses():
			self.kiosk_maps_list.append(fc)
		print self.kiosk_maps_list

		self.greely_DTA_gdb = r"F:\Anthony\Projects\Recreation\Kiosk Maps\1. GIS data\Fort_Greely_Satellite_Data.gdb"
		self.greely_DTA_list = []
		arcpy.env.workspace = self.greely_DTA_gdb
		for dataset in arcpy.ListDatasets():
			for fc in arcpy.ListFeatureClasses("*", "ALL", dataset):
				fcList.append(fc)
		for fc in arcpy.ListFeatureClasses():
			self.greely_DTA_list.append(fc)
		print self.greely_DTA_list

		self.woodcutting_gdb = r"F:\Anthony\Projects\Recreation\Wood Cutting\1. GIS data\WoodCutting.gdb"
		self.woodcutting_list = []
		arcpy.env.workspace = self.woodcutting_gdb
		for dataset in arcpy.ListDatasets():
			for fc in arcpy.ListFeatureClasses("*", "ALL", dataset):
				fcList.append(fc)
		for fc in arcpy.ListFeatureClasses():
			self.woodcutting_list.append(fc)
		print self.woodcutting_list

		# self.Greely_gdb = r"F:\Anthony\Projects\GIS\SDSFIE\FortGreely_SDE_40.gdb"
		# self.Greely_list = []
		# arcpy.env.workspace = self.Greely_gdb
		# for dataset in arcpy.ListDatasets():
		# 	for fc in arcpy.ListFeatureClasses("*", "ALL", dataset):
		# 		fcList.append(fc)
		# for fc in arcpy.ListFeatureClasses():
		# 	self.Greely_list.append(fc)
		# print self.Greely_list

		self.hillshade_gdb = r"F:\Anthony\GIS\Rasters\FWA_AK_Rasters.gdb"
		self.hillshade_list = []
		arcpy.env.workspace = self.hillshade_gdb
		for dataset in arcpy.ListDatasets():
			self.hillshade_list.append(dataset)
		print self.hillshade_list
		
		self.DOT_gdb = r"F:\Anthony\Projects\GIS\Vectors\DOT.gdb"
		# self.DOT_list = []
		# arcpy.env.workspace = self.DOT_gdb
		# for dataset in arcpy.ListDatasets():
		# 	for fc in arcpy.ListFeatureClasses("*", "ALL", dataset):
		# 		fcList.append(fc)
		# for fc in arcpy.ListFeatureClasses():
		# 	self.DOT_list.append(fc)
		# print self.DOT_list

		self.GMU_gdb = r"F:\Anthony\Projects\GIS\Vectors\ADFG.gdb"
		# self.GMU_list = []
		# arcpy.env.workspace = self.GMU_gdb
		# for dataset in arcpy.ListDatasets("GMU_07302020*", "Feature"):
		# 	for fc in arcpy.ListFeatureClasses("*", "ALL", dataset):
		# 		fcList.append(fc)
		# for fc in arcpy.ListFeatureClasses():
		# 	self.GMU_list.append(fc)
		# print self.GMU_list

		

		#KEEP BELOW
		# self.sdsfie_fcs = {}
		# arcpy.env.workspace = self.input_gdb
		# feature_datasets = arcpy.ListDatasets("*", "Feature")
		# for fd in feature_datasets:
		# 	new_workspace = self.input_gdb + "\\" + fd
		# 	arcpy.env.workspace = new_workspace
		# 	feature_classes  = arcpy.ListFeatureClasses()
		# 	for fc in feature_classes:
		# 		self.sdsfie_fcs[fc] = fd
		# print "finished feature list"
		# print self.sdsfie_fcs

	def fix_links(self):
		for root, dirs, files in os.walk(self.folder_path):
			for f in files:
				if f.endswith(".mxd"):
					maps = root + "\\" + f
					print "HERE WE GOOOOOOO" + maps
					mxd = arcpy.mapping.MapDocument(maps)
					df = arcpy.mapping.ListDataFrames(mxd)[0]
					broken_list = arcpy.mapping.ListBrokenDataSources(mxd)
					if not broken_list:
						print("\t" + "No broken data layers")
					else:
						print("\t" + "Contains broken data layers")
						for layer in arcpy.mapping.ListLayers(mxd, "", df):
							old_source = layer.dataSource
							if ".gdb" in old_source:
								old_source = old_source.split(".gdb")[0] + ".gdb"
							source_name = layer.datasetName
							if source_name in self.sdsfie_fcs:
								new_source = self.input_gdb
								if layer.supports("DATASOURCE"):
									layer.findAndReplaceWorkspacePath(old_source, new_source)

							elif source_name in self.general_layers_list:
								arcpy.env.workspace = self.general_layers_gdb
								new_source2 = self.general_layers_gdb
								layer.replaceDataSource(new_source2, "FILEGDB_WORKSPACE", source_name, False)

							elif source_name in self.kiosk_maps_list:
								arcpy.env.workspace = self.kiosk_maps_gdb
								new_source3 = self.kiosk_maps_gdb
								layer.replaceDataSource(new_source3, "FILEGDB_WORKSPACE", source_name, False)

							elif source_name in self.greely_DTA_list:
								arcpy.env.workspace = self.greely_DTA_gdb
								new_source4 = self.greely_DTA_gdb
								layer.replaceDataSource(new_source4, "FILEGDB_WORKSPACE", source_name, False)

							elif source_name in self.woodcutting_list:
								arcpy.env.workspace = self.woodcutting_gdb
								new_source5 = self.woodcutting_gdb
								layer.replaceDataSource(new_source5, "FILEGDB_WORKSPACE", source_name, False)

							# elif source_name in self.Greely_list:
							# 	arcpy.env.workspace = self.Greely_gdb
							# 	new_source6 = self.Greely_gdb
							# 	layer.replaceDataSource(new_source6, "FILEGDB_WORKSPACE", source_name, False)

							elif source_name in self.hillshade_list:
								arcpy.env.workspace = self.hillshade_gdb
								new_source7 = self.hillshade_gdb
								layer.replaceDataSource(new_source7, "FILEGDB_WORKSPACE", source_name, False)

							# elif source_name in self.DOT_list:
							# 	arcpy.env.workspace = self.DOT_gdb
							# 	new_source8 = self.DOT_gdb
							# 	layer.replaceDataSource(new_source8, "FILEGDB_WORKSPACE", source_name, False)

							# elif "Mile" in source_name:
							# 	print old_source
							# 	print source_name
							# 	new_source8 = self.DOT_gdb + "\\" + "Mileposts_091318"
							# 	print new_source8
							# 	layer.replaceDataSource(new_source8, "FILEGDB_WORKSPACE", source_name, False)
							# 	# layer.findAndReplaceWorkspacePath(old_source, new_source8)

							# # elif source_name in self.GMU_list:
							# # 	arcpy.env.workspace = self.GMU_gdb
							# # 	new_source9 = self.GMU_gdb
							# # 	layer.replaceDataSource(new_source9, "FILEGDB_WORKSPACE", source_name, False)

							# elif "GMU" in source_name:
							# 	new_source9 = self.GMU_gdb
							# 	layer.replaceDataSource(new_source9, "FILEGDB_WORKSPACE", source_name, False)
							# 	# layer.findAndReplaceWorkspacePath(old_source, new_source9)

					for logo in arcpy.mapping.ListLayoutElements(mxd, "PICTURE_ELEMENT"):
						if logo.name == "FWA_Insignia_242":
							logo.sourceImage = r"F:\Anthony\GIS\Templates\FWA_Insignia_gray.jpg"
						if logo.name == "amc-shield":
							logo.sourceImage = r"F:\Anthony\GIS\Templates\amc_shield_gray.jpg"
						if logo.name == "SCAREBEAR_Transparent":
							logo.sourceImage = r"F:\Anthony\GIS\Templates\SCAREBEAR_gray.jpg"
					arcpy.RefreshTOC()
					mxd.save()
					del mxd

	def fix_links2(self):
		for root, dirs, files in os.walk(self.folder_path):
			for f in files:
				if f.endswith(".mxd"):
					maps = root + "\\" + f
					print "HERE WE GOOOOOOO" + maps
					mxd = arcpy.mapping.MapDocument(maps)
					df = arcpy.mapping.ListDataFrames(mxd)[1]
					broken_list = arcpy.mapping.ListBrokenDataSources(mxd)
					if not broken_list:
						print("\t" + "No broken data layers")
					else:
						print("\t" + "Contains broken data layers")
						for layer in arcpy.mapping.ListLayers(mxd, "", df):
							old_source = layer.dataSource
							# print "Old source is: " + old_source
							if ".gdb" in old_source:
								old_source = old_source.split(".gdb")[0] + ".gdb"
							source_name = layer.datasetName
							if source_name in self.sdsfie_fcs:
								# new_source = self.input_gdb + "\\" + self.sdsfie_fcs[source_name] + "\\" + source_name
								new_source = self.input_gdb
								if layer.supports("DATASOURCE"):
									layer.findAndReplaceWorkspacePath(old_source, new_source)

							elif source_name in self.general_layers_list:
								arcpy.env.workspace = self.general_layers_gdb
								new_source2 = self.general_layers_gdb
								layer.replaceDataSource(new_source2, "FILEGDB_WORKSPACE", source_name, False)

							elif source_name in self.kiosk_maps_list:
								arcpy.env.workspace = self.kiosk_maps_gdb
								new_source3 = self.kiosk_maps_gdb
								layer.replaceDataSource(new_source3, "FILEGDB_WORKSPACE", source_name, False)

							elif source_name in self.greely_DTA_list:
								arcpy.env.workspace = self.greely_DTA_gdb
								new_source4 = self.greely_DTA_gdb
								layer.replaceDataSource(new_source4, "FILEGDB_WORKSPACE", source_name, False)

							elif source_name in self.woodcutting_list:
								arcpy.env.workspace = self.woodcutting_gdb
								new_source5 = self.woodcutting_gdb
								layer.replaceDataSource(new_source5, "FILEGDB_WORKSPACE", source_name, False)

							# elif source_name in self.Greely_list:
							# 	arcpy.env.workspace = self.Greely_gdbe
							# 	new_source6 = self.Greely_gdb
							# 	layer.replaceDataSource(new_source6, "FILEGDB_WORKSPACE", source_name, False)

							elif source_name in self.hillshade_list:
								arcpy.env.workspace = self.hillshade_gdb
								new_source7 = self.hillshade_gdb
								layer.replaceDataSource(new_source7, "FILEGDB_WORKSPACE", source_name, False)

							# elif source_name in self.DOT_list:
							# 	arcpy.env.workspace = self.DOT_gdb
							# 	new_source8 = self.DOT_gdb
							# 	layer.replaceDataSource(new_source8, "FILEGDB_WORKSPACE", source_name, False)

							# elif "Mile" in source_name:
							# 	new_source8 = self.DOT_gdb
							# 	layer.replaceDataSource(new_source8, "FILEGDB_WORKSPACE", source_name, False)
							# 	# layer.findAndReplaceWorkspacePath(old_source, new_source8)

							# # elif source_name in self.GMU_list:
							# # 	arcpy.env.workspace = self.GMU_gdb
							# # 	new_source9 = self.GMU_gdb
							# # 	layer.replaceDataSource(new_source9, "FILEGDB_WORKSPACE", source_name, False)

							# elif "GMU" in source_name:
							# 	new_source9 = self.GMU_gdb
							# 	layer.replaceDataSource(new_source9, "FILEGDB_WORKSPACE", source_name, False)
							# 	# layer.findAndReplaceWorkspacePath(old_source, new_source9)

					arcpy.RefreshTOC()
					mxd.save()
					del mxd

	def fix_links3(self):
		for root, dirs, files in os.walk(self.folder_path):
			for f in files:
				if f.endswith(".mxd"):
					maps = root + "\\" + f
					print "HERE WE GOOOOOOO" + maps
					mxd = arcpy.mapping.MapDocument(maps)
					df = arcpy.mapping.ListDataFrames(mxd)[2]
					broken_list = arcpy.mapping.ListBrokenDataSources(mxd)
					if not broken_list:
						print("\t" + "No broken data layers")
					else:
						print("\t" + "Contains broken data layers")
						for layer in arcpy.mapping.ListLayers(mxd, "", df):
							old_source = layer.dataSource
							# print "Old source is: " + old_source
							if ".gdb" in old_source:
								old_source = old_source.split(".gdb")[0] + ".gdb"
							source_name = layer.datasetName
							if source_name in self.sdsfie_fcs:
								# new_source = self.input_gdb + "\\" + self.sdsfie_fcs[source_name] + "\\" + source_name
								new_source = self.input_gdb
								if layer.supports("DATASOURCE"):
									layer.findAndReplaceWorkspacePath(old_source, new_source)

							elif source_name in self.general_layers_list:
								arcpy.env.workspace = self.general_layers_gdb
								new_source2 = self.general_layers_gdb
								layer.replaceDataSource(new_source2, "FILEGDB_WORKSPACE", source_name, False)

							elif source_name in self.kiosk_maps_list:
								arcpy.env.workspace = self.kiosk_maps_gdb
								new_source3 = self.kiosk_maps_gdb
								layer.replaceDataSource(new_source3, "FILEGDB_WORKSPACE", source_name, False)

							elif source_name in self.greely_DTA_list:
								arcpy.env.workspace = self.greely_DTA_gdb
								new_source4 = self.greely_DTA_gdb
								layer.replaceDataSource(new_source4, "FILEGDB_WORKSPACE", source_name, False)

							elif source_name in self.woodcutting_list:
								arcpy.env.workspace = self.woodcutting_gdb
								new_source5 = self.woodcutting_gdb
								layer.replaceDataSource(new_source5, "FILEGDB_WORKSPACE", source_name, False)

							# elif source_name in self.Greely_list:
							# 	arcpy.env.workspace = self.Greely_gdbe
							# 	new_source6 = self.Greely_gdb
							# 	layer.replaceDataSource(new_source6, "FILEGDB_WORKSPACE", source_name, False)

							elif source_name in self.hillshade_list:
								arcpy.env.workspace = self.hillshade_gdb
								new_source7 = self.hillshade_gdb
								layer.replaceDataSource(new_source7, "FILEGDB_WORKSPACE", source_name, False)

							# elif source_name in self.DOT_list:
							# 	arcpy.env.workspace = self.DOT_gdb
							# 	new_source8 = self.DOT_gdb
							# 	layer.replaceDataSource(new_source8, "FILEGDB_WORKSPACE", source_name, False)

							# elif "Mile" in source_name:
							# 	new_source8 = self.DOT_gdb
							# 	layer.replaceDataSource(new_source8, "FILEGDB_WORKSPACE", source_name, False)
							# 	# layer.findAndReplaceWorkspacePath(old_source, new_source8)

							# # elif source_name in self.GMU_list:
							# # 	arcpy.env.workspace = self.GMU_gdb
							# # 	new_source9 = self.GMU_gdb
							# # 	layer.replaceDataSource(new_source9, "FILEGDB_WORKSPACE", source_name, False)

							# elif "GMU" in source_name:
							# 	new_source9 = self.GMU_gdb
							# 	layer.replaceDataSource(new_source9, "FILEGDB_WORKSPACE", source_name, False)
							# 	# layer.findAndReplaceWorkspacePath(old_source, new_source9)

					arcpy.RefreshTOC()
					mxd.save()
					del mxd

	def fix_links4(self):
		for root, dirs, files in os.walk(self.folder_path):
			for f in files:
				if f.endswith(".mxd"):
					maps = root + "\\" + f
					print "HERE WE GOOOOOOO" + maps
					mxd = arcpy.mapping.MapDocument(maps)
					df = arcpy.mapping.ListDataFrames(mxd)[3]
					broken_list = arcpy.mapping.ListBrokenDataSources(mxd)
					if not broken_list:
						print("\t" + "No broken data layers")
					else:
						print("\t" + "Contains broken data layers")
						for layer in arcpy.mapping.ListLayers(mxd, "", df):
							old_source = layer.dataSource
							# print "Old source is: " + old_source
							if ".gdb" in old_source:
								old_source = old_source.split(".gdb")[0] + ".gdb"
							source_name = layer.datasetName
							if source_name in self.sdsfie_fcs:
								# new_source = self.input_gdb + "\\" + self.sdsfie_fcs[source_name] + "\\" + source_name
								new_source = self.input_gdb
								if layer.supports("DATASOURCE"):
									layer.findAndReplaceWorkspacePath(old_source, new_source)

							elif source_name in self.general_layers_list:
								arcpy.env.workspace = self.general_layers_gdb
								new_source2 = self.general_layers_gdb
								layer.replaceDataSource(new_source2, "FILEGDB_WORKSPACE", source_name, False)

							elif source_name in self.kiosk_maps_list:
								arcpy.env.workspace = self.kiosk_maps_gdb
								new_source3 = self.kiosk_maps_gdb
								layer.replaceDataSource(new_source3, "FILEGDB_WORKSPACE", source_name, False)

							elif source_name in self.greely_DTA_list:
								arcpy.env.workspace = self.greely_DTA_gdb
								new_source4 = self.greely_DTA_gdb
								layer.replaceDataSource(new_source4, "FILEGDB_WORKSPACE", source_name, False)
							elif source_name in self.woodcutting_list:
								arcpy.env.workspace = self.woodcutting_gdb
								new_source5 = self.woodcutting_gdb
								layer.replaceDataSource(new_source5, "FILEGDB_WORKSPACE", source_name, False)

							# elif source_name in self.Greely_list:
							# 	arcpy.env.workspace = self.Greely_gdbe
							# 	new_source6 = self.Greely_gdb
							# 	layer.replaceDataSource(new_source6, "FILEGDB_WORKSPACE", source_name, False)

							elif source_name in self.hillshade_list:
								arcpy.env.workspace = self.hillshade_gdb
								new_source7 = self.hillshade_gdb
								layer.replaceDataSource(new_source7, "FILEGDB_WORKSPACE", source_name, False)

							# elif source_name in self.DOT_list:
							# 	arcpy.env.workspace = self.DOT_gdb
							# 	new_source8 = self.DOT_gdb
							# 	layer.replaceDataSource(new_source8, "FILEGDB_WORKSPACE", source_name, False)

							# elif "Mile" in source_name:
							# 	new_source8 = self.DOT_gdb
							# 	layer.replaceDataSource(new_source8, "FILEGDB_WORKSPACE", source_name, False)
							# 	# layer.findAndReplaceWorkspacePath(old_source, new_source8)

							# # elif source_name in self.GMU_list:
							# # 	arcpy.env.workspace = self.GMU_gdb
							# # 	new_source9 = self.GMU_gdb
							# # 	layer.replaceDataSource(new_source9, "FILEGDB_WORKSPACE", source_name, False)

							# elif "GMU" in source_name:
							# 	new_source9 = self.GMU_gdb
							# 	layer.replaceDataSource(new_source9, "FILEGDB_WORKSPACE", source_name, False)
							# 	# layer.findAndReplaceWorkspacePath(old_source, new_source9)


					arcpy.RefreshTOC()
					mxd.save()
					del mxd
	def fix_links5(self):
		for root, dirs, files in os.walk(self.folder_path):
			for f in files:
				if f.endswith(".mxd"):
					maps = root + "\\" + f
					print "HERE WE GOOOOOOO" + maps
					mxd = arcpy.mapping.MapDocument(maps)
					df = arcpy.mapping.ListDataFrames(mxd)[4]
					broken_list = arcpy.mapping.ListBrokenDataSources(mxd)
					if not broken_list:
						print("\t" + "No broken data layers")
					else:
						print("\t" + "Contains broken data layers")
						for layer in arcpy.mapping.ListLayers(mxd, "", df):
							old_source = layer.dataSource
							# print "Old source is: " + old_source
							if ".gdb" in old_source:
								old_source = old_source.split(".gdb")[0] + ".gdb"
							source_name = layer.datasetName
							if source_name in self.sdsfie_fcs:
								# new_source = self.input_gdb + "\\" + self.sdsfie_fcs[source_name] + "\\" + source_name
								new_source = self.input_gdb
								if layer.supports("DATASOURCE"):
									layer.findAndReplaceWorkspacePath(old_source, new_source)

							elif source_name in self.general_layers_list:
								arcpy.env.workspace = self.general_layers_gdb
								new_source2 = self.general_layers_gdb
								layer.replaceDataSource(new_source2, "FILEGDB_WORKSPACE", source_name, False)

							elif source_name in self.kiosk_maps_list:
								arcpy.env.workspace = self.kiosk_maps_gdb
								new_source3 = self.kiosk_maps_gdb
								layer.replaceDataSource(new_source3, "FILEGDB_WORKSPACE", source_name, False)

							elif source_name in self.greely_DTA_gdb:
								arcpy.env.workspace = self.greely_DTA_gdb
								new_source4 = self.greely_DTA_gdb
								layer.replaceDataSource(new_source4, "FILEGDB_WORKSPACE", source_name, False)

							elif source_name in self.woodcutting_list:
								arcpy.env.workspace = self.woodcutting_gdb
								new_source5 = self.woodcutting_gdb
								layer.replaceDataSource(new_source5, "FILEGDB_WORKSPACE", source_name, False)

							# elif source_name in self.Greely_list:
							# 	arcpy.env.workspace = self.Greely_gdbe
							# 	new_source6 = self.Greely_gdb
							# 	layer.replaceDataSource(new_source6, "FILEGDB_WORKSPACE", source_name, False)

							elif source_name in self.hillshade_list:
								arcpy.env.workspace = self.hillshade_gdb
								new_source7 = self.hillshade_gdb
								layer.replaceDataSource(new_source7, "FILEGDB_WORKSPACE", source_name, False)

							# elif source_name in self.DOT_list:
							# 	arcpy.env.workspace = self.DOT_gdb
							# 	new_source8 = self.DOT_gdb
							# 	layer.replaceDataSource(new_source8, "FILEGDB_WORKSPACE", source_name, False)

							# elif "Mile" in source_name:
							# 	new_source8 = self.DOT_gdb
							# 	layer.replaceDataSource(new_source8, "FILEGDB_WORKSPACE", source_name, False)
							# 	# layer.findAndReplaceWorkspacePath(old_source, new_source8)

							# # elif source_name in self.GMU_list:
							# # 	arcpy.env.workspace = self.GMU_gdb
							# # 	new_source9 = self.GMU_gdb
							# # 	layer.replaceDataSource(new_source9, "FILEGDB_WORKSPACE", source_name, False)

							# elif "GMU" in source_name:
							# 	new_source9 = self.GMU_gdb
							# 	layer.replaceDataSource(new_source9, "FILEGDB_WORKSPACE", source_name, False)
							# 	# layer.findAndReplaceWorkspacePath(old_source, new_source9)

					arcpy.RefreshTOC()
					mxd.save()
					del mxd

	def fix_links6(self):
		for root, dirs, files in os.walk(self.folder_path):
			for f in files:
				if f.endswith(".mxd"):
					maps = root + "\\" + f
					print "HERE WE GOOOOOOO" + maps
					mxd = arcpy.mapping.MapDocument(maps)
					df = arcpy.mapping.ListDataFrames(mxd)[5]
					broken_list = arcpy.mapping.ListBrokenDataSources(mxd)
					if not broken_list:
						print("\t" + "No broken data layers")
					else:
						print("\t" + "Contains broken data layers")
						for layer in arcpy.mapping.ListLayers(mxd, "", df):
							old_source = layer.dataSource
							# print "Old source is: " + old_source
							if ".gdb" in old_source:
								old_source = old_source.split(".gdb")[0] + ".gdb"
							source_name = layer.datasetName
							if source_name in self.sdsfie_fcs:
								# new_source = self.input_gdb + "\\" + self.sdsfie_fcs[source_name] + "\\" + source_name
								new_source = self.input_gdb
								if layer.supports("DATASOURCE"):
									layer.findAndReplaceWorkspacePath(old_source, new_source)

							elif source_name in self.general_layers_list:
								arcpy.env.workspace = self.general_layers_gdb
								new_source2 = self.general_layers_gdb
								layer.replaceDataSource(new_source2, "FILEGDB_WORKSPACE", source_name, False)

							elif source_name in self.kiosk_maps_list:
								arcpy.env.workspace = self.kiosk_maps_gdb
								new_source3 = self.kiosk_maps_gdb
								layer.replaceDataSource(new_source3, "FILEGDB_WORKSPACE", source_name, False)

							# elif source_name in self.Greely_list:
							# 	arcpy.env.workspace = self.Greely_gdbe
							# 	new_source6 = self.Greely_gdb
							# 	layer.replaceDataSource(new_source6, "FILEGDB_WORKSPACE", source_name, False)

							elif source_name in self.woodcutting_list:
								arcpy.env.workspace = self.woodcutting_gdb
								new_source5 = self.woodcutting_gdb
								layer.replaceDataSource(new_source5, "FILEGDB_WORKSPACE", source_name, False)

							# elif source_name in self.Greely_list:
							# 	arcpy.env.workspace = self.Greely_gdbe
							# 	new_source6 = self.Greely_gdb
							# 	layer.replaceDataSource(new_source6, "FILEGDB_WORKSPACE", source_name, False)

							elif source_name in self.hillshade_list:
								arcpy.env.workspace = self.hillshade_gdb
								new_source7 = self.hillshade_gdb
								layer.replaceDataSource(new_source7, "FILEGDB_WORKSPACE", source_name, False)

							# elif source_name in self.DOT_list:
							# 	arcpy.env.workspace = self.DOT_gdb
							# 	new_source8 = self.DOT_gdb
							# 	layer.replaceDataSource(new_source8, "FILEGDB_WORKSPACE", source_name, False)

							# elif "Mile" in source_name:
							# 	new_source8 = self.DOT_gdb
							# 	layer.replaceDataSource(new_source8, "FILEGDB_WORKSPACE", source_name, False)
							# 	# layer.findAndReplaceWorkspacePath(old_source, new_source8)

							# # elif source_name in self.GMU_list:
							# # 	arcpy.env.workspace = self.GMU_gdb
							# # 	new_source9 = self.GMU_gdb
							# # 	layer.replaceDataSource(new_source9, "FILEGDB_WORKSPACE", source_name, False)

							# elif "GMU" in source_name:
							# 	new_source9 = self.GMU_gdb
							# 	layer.replaceDataSource(new_source9, "FILEGDB_WORKSPACE", source_name, False)
							# 	# layer.findAndReplaceWorkspacePath(old_source, new_source9)


					arcpy.RefreshTOC()
					mxd.save()
					del mxd

if __name__ == "__main__":
	folder_path = r"F:\Anthony\Projects\Recreation\Kiosk Maps\2. MXDs\Rec_Maps\Satellite_Versions_New"
	input_gdb = r"F:\Anthony\GIS\SDSFIE\FWA_SDE_40_20200323.gdb"
	find_fix = FindFix_MXDs(folder_path, input_gdb)
	find_fix.feature_list()
	find_fix.fix_links()
	find_fix.fix_links2()
	find_fix.fix_links3()
	find_fix.fix_links4()
	find_fix.fix_links5()
	find_fix.fix_links6()