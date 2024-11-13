import random
import json
import string
from enum import Enum, auto
from itertools import chain
from typing import Optional

from biocypher._create import BioCypherNode, BioCypherEdge
from biocypher._logger import logger

logger.debug(f"Loading module {__name__}.")


class BrapiAdapterNodeType(Enum):
    """
    Define types of nodes the adapter can provide.
    """

    TRIAL = auto()
    STUDY = auto()
    GERMPLASM = auto()


class BrapiAdapterTrialField(Enum):
    trialDbId = "trialDbId"
    trialName = "trialName"
    studies = "studies"


class BrapiAdapterStudyField(Enum):
    studyDbId = "studyDbId"
    studyName = "studyName"
    trialName = "trialName"
    germplasmDbIds = "germplasmDbIds"


class BrapiAdapterGermplasmField(Enum):
    GERMPLASMDBID = "germplasmDbId"
    GERMPLASMName = "germplasmName"


class BrapiAdapterEdgeType(Enum):
    TRIAL_STUDIES = "trial_studies"
    STUDIES_GERMPLASM = "studies_germplasm"



class BrapiAdapter:
    """


    Args:
        node_types: List of node types to include in the result.
        node_fields: List of node fields to include in the result.
        edge_types: List of edge types to include in the result.
        edge_fields: List of edge fields to include in the result.
    """

    def __init__(
        self,
        node_types: Optional[list] = None,
        node_fields: Optional[list] = None,
        edge_types: Optional[list] = None,
        edge_fields: Optional[list] = None,
    ):
        self._set_types_and_fields(node_types, node_fields, edge_types, edge_fields)
        self._preprocess_data()

    """
    see https://github.com/biocypher/collectri/blob/main/collectri/adapters/collectri_adapter.py
    """
    def _preprocess_data(self):
        logger.info("loading json source data in memory")
        # load json data from brapiDataPopyWheat/germplasm.json
        with open("brapiDataPopyWheat/germplasm.json", 'r') as file:
            self.germplasm = json.load(file)
        # load json data from brapiDataPopyWheat study.json
        with open("brapiDataPopyWheat/study.json", 'r') as file:
            self.study = json.load(file)
        # load json data from brapiDataPopyWheat trial.json
        with open("brapiDataPopyWheat/trial.json", 'r') as file:
            self.trial = json.load(file)

    def get_nodes(self):
        logger.info("Generating nodes.")

        for trial in self.trial:
            yield BioCypherNode (
                node_id=trial["trialDbId"],
                node_label="trial",
                properties={
                    "trialDbId": trial["trialDbId"],
                    "trialName": trial["trialName"],
                    "documentationURL": trial["documentationURL"]
                }
            )

        for study in self.study:
            properties={
                "studyDbId": study["studyDbId"],
                "studyName": study["studyName"],
                "trialName": study["trialName"],
                "germplasmDbIds": study["germplasmDbIds"],
                "startDate": study["startDate"],
                "endDate": study["endDate"],
                "documentationURL": study["documentationURL"],
                "studyType": study["studyType"],
                "locationName": study["locationName"],
                "locationDbId": study["locationDbId"],
                "observationVariableDbIds": study["observationVariableDbIds"],
                "seasons": study["seasons"]
            }
            #yield (study["studyDbId"], "study", properties)
            yield BioCypherNode (
               node_id=study["studyDbId"],
               node_label="study",
               properties=properties,
            )

        for germplasm in self.germplasm:
            properties={
                "germplasmDbId": germplasm["germplasmDbId"],
                "germplasmName": germplasm["germplasmName"],
                "germplasmPUI": germplasm["germplasmPUI"],
                "accessionNumber": germplasm["accessionNumber"],
                "instituteCode": germplasm["instituteCode"],
                "instituteName": germplasm["instituteName"],
                "biologicalStatusOfAccessionCode": germplasm["biologicalStatusOfAccessionCode"],
                "biologicalStatusOfAccessionDescription": germplasm["biologicalStatusOfAccessionDescription"],
                "countryOfOriginCode": germplasm["countryOfOriginCode"],
                "pedigree": germplasm["pedigree"],
                "genusSpecies": germplasm["genusSpecies"],
                #"synonyms": germplasm["synonyms"],
                "genus": germplasm["genus"],
                "species": germplasm["species"],
                "subtaxa": germplasm["subtaxa"],
                "presenceStatus": germplasm["presenceStatus"],
                "commonCropName": germplasm["commonCropName"],
                "taxonCommonNames": germplasm["taxonCommonNames"]
            }
            yield BioCypherNode (
                node_id=germplasm["germplasmDbId"],
                node_label="germplasm",
                properties=properties,
            )

    def get_edges(self):
        logger.info("Generating edges.")

        for trial in self.trial:
            for study in trial["studies"]:
                yield BioCypherEdge (
                    source_id=trial["trialDbId"],
                    target_id=study["studyDbId"],
                    relationship_label="trial_studies",
                    properties={}
                )

        for study in self.study:
            for germplasm in study["germplasmDbIds"]:
                yield BioCypherEdge (
                    source_id=study["studyDbId"],
                    target_id=germplasm,
                    relationship_label="studies_germplasm",
                    properties={}
                )

    def get_node_count(self):
        """
        Returns the number of nodes generated by the adapter.
        """
        return len(list(self.get_nodes()))

    def _set_types_and_fields(self, node_types, node_fields, edge_types, edge_fields):
        if node_types:
            self.node_types = node_types
        else:
            self.node_types = [type for type in BrapiAdapterNodeType]

        if node_fields:
            self.node_fields = node_fields
        else:
            self.node_fields = [
                field
                for field in chain(
                    BrapiAdapterStudyField,
                    BrapiAdapterTrialField,
                    BrapiAdapterGermplasmField,
                )
            ]

        if edge_types:
            self.edge_types = edge_types
        else:
            self.edge_types = [type for type in BrapiAdapterEdgeType]

        if edge_fields:
            self.edge_fields = edge_fields
        else:
            self.edge_fields = [field for field in chain()]

