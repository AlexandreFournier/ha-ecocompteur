"""Helper functions for the Ecocompteur."""

import httpx
from homeassistant.core import HomeAssistant
from homeassistant.helpers.httpx_client import get_async_client


class EcocompteurApiError(Exception):
    """Ecocompteur client exception."""


STATUS_CODE_OK = 200


class Ecocompteur:
    """Ecocompteur client."""

    def __init__(self, hass: HomeAssistant, host: str) -> None:
        """Initialize an Ecocompteur client."""
        self.hass = hass
        self.host = host

    async def _fetch(self, name: str) -> httpx.Response:
        uri = f"http://{self.host}/{name}"
        try:
            async_client = get_async_client(self.hass)
            r = await async_client.get(uri, timeout=5)
            if r.status_code != STATUS_CODE_OK:
                raise EcocompteurApiError
        except httpx.ConnectTimeout as e:
            raise EcocompteurApiError from e
        except httpx.ConnectError as e:
            raise EcocompteurApiError from e
        else:
            return r

    async def fetch_data(self) -> dict:
        """
        Fetch Ecocompteur general data.

        This is the expected JSON format:

        {
            "option_tarifaire" : 4,
            "tarif_courant" : 11,
            "isousc" : 0,

            "conso_base" : 0,
            "conso_hc"   : 0,
            "conso_hp"   : 0,
            "conso_hc_b" : 0,
            "conso_hp_b" : 0,
            "conso_hc_w" : 0,
            "conso_hp_w" : 0,
            "conso_hc_r" : 0,
            "conso_hp_r" : 0,

            "type_imp_0" : 1,
            "type_imp_1" : 1,
            "type_imp_2" : 1,
            "type_imp_3" : 1,
            "type_imp_4" : 1,
            "type_imp_5" : 1,

            "label_entree1" : "Consommation globale",
            "label_entree2" : "Cumulus             ",
            "label_entree3" : "Cuisine             ",
            "label_entree4" : "Prises de Courant",
            "label_entree5" : "Informatique        ",

            "label_entree_imp0" : "Eau",
            "label_entree_imp1" : "Eau",
            "label_entree_imp2" : "Eau",
            "label_entree_imp3" : "Eau",
            "label_entree_imp4" : "Eau",
            "label_entree_imp5" : "Eau",

            "entree_imp0_disabled" : 0,
            "entree_imp1_disabled" : 1,
            "entree_imp2_disabled" : 1,
            "entree_imp3_disabled" : 1,
            "entree_imp4_disabled" : 1,
            "entree_imp5_disabled" : 1
        }

        Return a well-structured dictionary like this:

        {
            "option_tarifaire" : 4,
            "tarif_courant" : 11,
            "isousc" : 0,
            "conso": {
                "base" : 0,
                "hc"   : 0,
                "hp"   : 0,
                "hc_b" : 0,
                "hp_b" : 0,
                "hc_w" : 0,
                "hp_w" : 0,
                "hc_r" : 0,
                "hp_r" : 0,
            },
            "entree": [
                {
                    "label": "Consommation globale",
                    "type" : 0,
                    "disabled" : false,
                },
                {
                    "label": "Cumulus",
                    "type" : 0
                    "disabled" : false,
                },
                {
                    "label": "Cuisine",
                    "type" : 0
                    "disabled" : false,
                },
                {
                    "label": "Prises de Courant",
                    "type" : 0
                    "disabled" : false,
                },
                {
                    "label": "Informatique",
                    "type" : 0
                    "disabled" : false,
                },
                {
                    "label" : "Eau",
                    "type" : 1,
                    "disabled" : 0,
                },
                {
                    "label" : "Eau",
                    "type" : 1,
                    "disabled" : 1,
                },
                {
                    "label" : "Eau",
                    "type" : 1,
                    "disabled" : 1,
                },
                {
                    "label" : "Eau",
                    "type" : 1,
                    "disabled" : 1,
                },
                {
                    "label" : "Eau",
                    "type" : 1,
                    "disabled" : 1,
                },
                {
                    "label" : "Eau",
                    "type" : 1,
                    "disabled" : 1
                },
            ]
        }
        """
        r = await self._fetch("data.json")
        j = r.json()
        ret = {
            "option_tarifaire": j["option_tarifaire"],
            "tarif_courant": j["tarif_courant"],
            "isousc": j["isousc"],
            "conso": {
                "base": j["conso_base"],
                "hc": j["conso_hc"],
                "hp": j["conso_hp"],
                "hc_b": j["conso_hc_b"],
                "hp_b": j["conso_hp_b"],
                "hc_w": j["conso_hc_w"],
                "hp_w": j["conso_hp_w"],
                "hc_r": j["conso_hc_r"],
                "hp_r": j["conso_hp_r"],
            },
            "inputs": [],
        }
        for i in range(1, 6):
            label = j[f"label_entree{i}"].strip()
            ret["inputs"].append({"label": label, "type": 0, "disabled": False})
        for i in range(6):
            label = j[f"label_entree_imp{i}"].strip()
            stype = j[f"type_imp_{i}"]
            disabled = bool(j[f"entree_imp{i}_disabled"])
            if disabled:
                label = "N/A"
            ret["inputs"].append({"label": label, "type": stype, "disabled": disabled})
        return ret

    async def fetch_inst(self) -> dict:
        """
        Fetch Ecocompteur real-time data.

        This is the expected JSON format:
        {
            "data1":178.000000,
            "data2":0.000000,
            "data3":0.000000,
            "data4":0.000000,
            "data5":79.000000,
            "data6":64.903999,
            "data6m3":64.903999,
            "data7":0.000000,
            "data7m3":0.000000,
            "heure":10,
            "minute":40,
            "CIR1_Nrj":0.000000,
            "CIR1_Vol":0.000000,
            "CIR2_Nrj":0.000000,
            "CIR2_Vol":0.000000,
            "CIR3_Nrj":0.000000,
            "CIR3_Vol":0.000000,
            "CIR4_Nrj":0.000000,
            "CIR4_Vol":0.000000,
            "Date_Time":1727865642
        }
        """
        r = await self._fetch("inst.json")
        return r.json()

    async def fetch_log1(self) -> str:
        """Fetch Ecocompteur statistics."""
        r = await self._fetch("log1.csv")
        return r.text

    async def fetch_log2(self) -> str:
        """Fetch Ecocompteur statistics."""
        r = await self._fetch("log2.csv")
        return r.text
