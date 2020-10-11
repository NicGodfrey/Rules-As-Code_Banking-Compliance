unitTesting = False
sectionsCovered = "sections 126-133 of the National Consumer Credit Protection Act 2009"
consideredLaw = sectionsCovered
daysInYear = 365 #TODO DEFINE A YEAR
ASIC_160F_131 = daysInYear*3 #ASIC Credit (Unsuitability -- Credit Cards) Instrument 2018/753
bodyCorporate = ["corporate", "trust", "body corporate", "corporation", "other", "corporate body", "partnership", "company", "LLC", "bank", "credit union"]
individualTypes = ["natural person", "person", "individual", "human"]


""" This program considers the following legal texts:
 -- Acts Interpretation Act 1901 (Cth) ss 2, 2C, 40A
 -- Banking Act 1959 (Cth) s 5
 -- Corporations Act 2001 (Cth) ss 9, 761A
 -- Crimes Act 1914 (Cth) s 4
 -- National Consumer Credit Protection Act 2009 (Cth) ss 126-133
 -- National Consumer Credit Protection Regulatioins 2010 (Cth) ss 28HA-28JA
 -- ASIC Credit (Unsuitability - Credit Cards) Instrument 2018/753
 -- Australian Securities and Investments Commission v Westpac Banking Corporation (2020) 380 ALR 262
 -- Australian Securities and Investments Commission v Cash Store Pty Ltd (in liquidation) [2014] FCA 926
 """

""" Limitations of this program include:
 -- Failure to account for time of incidents (eg. which legislative instruments are in force at given date)
 -- """

