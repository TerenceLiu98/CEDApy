## Fred

For the ST.Louis Fred data, we mainly focus on the ["Main Economic Indicators" Series](https://fred.stlouisfed.org/tags/series?t=mei)

```python
from CEDA.economic.Fred import *
usa = FredData(country="usa")
usa_toc = usa.toc()
data = usa.download_data(sid="LFAC24FEUSM647N")
```

## Eurostat

```python
from CEDA.economic.Eurostat import *
eurostat = EurostatData(language="en")
eurostat_toc = eurostat.toc()
GDP_related = eurostat.search_toc(query="GDP")
nama_10_gdp = eurostat.download_data(datasetcode="nama_10_gdp")
tet00004 = eurostat.download_data(datasetcode="tet00004")
```

## ECB

```python
from CEDA.economic.ECB import *
ecb = ECBData()
ecb_toc = ecb.toc()
AME = ecb.download_data(datasetname="AME")
```

## OECD

```python
from CEDA.economic.OECD import *
oecd = OECDData()
oecd_toc = oecd.toc()
oecd_tos = oecd.tos(dataset="QNA")
data = oecd.download_data(dataset="QNA", query="QNA/CAN.B1_GE.CQRSA.Q")
```

## NBSC

```python
from CEDA.economic.NBSC import *
nbsc = NBSCData(language="en", period="monthly")
nbsc_nodes = nbsc.tree_generation()
nbsc_toc = nbsc.toc(nodes=nbsc_nodes)
A010301 = nbsc.download_data(nid="A010301")
```

## Xinhua
```python
from CEDA.economic.XinHua import *
xhdata = XHData()
toc = xhdata.toc()
data = xhdata.download_data(iid=12006) # GDP
```

## BOJ

```python
from CEDA.economic.BOJ import *
boj = BOJData()
boj_toc = boj.toc()
survey = boj.download_data("Survey")
```

## EPU

```python
from CEDA.economic.EPU import * 
country_list, annotations = country_list()
can_epu = EPUData(country="Canada")
mainland_china_epu = EPUData(country="China")
can_data, can_reference = can_epu.download()
mainland_china_data, cn_reference = mainland_china_epu.download()
```