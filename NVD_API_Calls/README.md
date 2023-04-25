**CVSS SCORE AUTOMATION**

I was told in an interview that part of my job would be to make an API call, grab newly published CVEs,
and somehow find a way to calculate a CVSS score using a CVSS calculator

Fortunately, toolswatch on GitHub made a wonderful cvss calculator. I have written code that makes an API call to NVD
(NIST's National Vulnerability Database). This code will then write the returned json in pretty format, and
write an Excel sheet that has the original relevant data.

It will then use toolswatch's code to calculate it, then write a new Excel sheet with the newly calculated scores

Big shoutout to toolswatch and their code: https://github.com/toolswatch/pycvss3

Dependencies: openpyxl, art
