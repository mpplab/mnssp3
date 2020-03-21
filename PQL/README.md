# PQL
**Background:**
* Differential privacy protection technology can ensure that sensitive personal information will not be leaked when publishing aggregated data. As a necessary way to publish aggregated data, the query language's security should be taken seriously by us. This query language built into MNSSp3, called PQL, which is used to solve the privacy problem of summary data leakage.

**Method type:** build-in

**Method name:** PQL 

**usage:**  
* PROTECT table_name PICK fun[column] WITH ｛WITHRANGE(1,2) ｝｛GLOBAL WHERE (condition) ｝
* PROTECT、 PICK WITH ｛WITHRANGE(1,2) ｝ are required keywords. WITH and WITHRANGE requires us to choose one.
* GLOBAL is used with WHERE. It means that in the conditional query, the user can choose global or random sensitivity.
* PICK supports different functions: count()-Count[*], max()-Highest[column],min()-Lowest[column], average()-Avg[column], sum()-Total[column].
* The range of can be selected between (0, 1).

**Additional remarks:**
* You can try the query example on the right side of the MNSSp3 page to understand the PQL language input form.