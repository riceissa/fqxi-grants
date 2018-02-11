#!/usr/bin/env python3
# License: CC0 https://creativecommons.org/publicdomain/zero/1.0/

from bs4 import BeautifulSoup


DATA = [
        "data/2006.html",
        "data/2008.html",
        "data/2010.html",
        "data/2013.html",
        "data/2015.html",
        "data/2016.html",
        ]


def main():
    first = True
    print("""insert into donations (donor, donee, donation_earmark, amount, donation_date,
    donation_date_precision, donation_date_basis, cause_area, url,
    donor_cause_area_url, notes, affected_countries, affected_states,
    affected_cities, affected_regions) values""")

    for fp in DATA:
        with open(fp, "r") as f:
            soup = BeautifulSoup(f, "lxml")
            table = soup.find("table")
            for tr in table.find_all("tr"):
                cells = tr.find_all("td")
                awardee = cells[0].text.strip()
                if awardee in ["Awardee", "TOTAL", ""]:
                    continue
                grantee_url = "https://fqxi.org" + cells[0].a["href"]
                institution = cells[1].text.strip().replace(",", "")
                amount_text = cells[2].text.strip()
                assert amount_text.startswith("$")
                amount = float(amount_text.replace("$", "").replace(",", ""))
                title = cells[3].text.strip()
                print(("    " if first else "    ,") + "(" + ",".join([
                    mysql_quote("Foundational Questions Institute"),  # donor
                    mysql_quote(institution),  # donee
                    mysql_quote(awardee),  # donation_earmark
                    str(amount),  # amount
                    mysql_quote(fp[len("data/"):-len(".html")] + "-01-01"),  # donation_date
                    mysql_quote("year"),  # donation_date_precision
                    mysql_quote("donation log"),  # donation_date_basis
                    mysql_quote("FIXME"),  # cause_area
                    mysql_quote(grantee_url),  # url
                    mysql_quote(""),  # donor_cause_area_url
                    mysql_quote("Project title: " + title),  # notes
                    mysql_quote(""),  # affected_countries
                    mysql_quote(""),  # affected_states
                    mysql_quote(""),  # affected_cities
                    mysql_quote(""),  # affected_regions
                ]) + ")")
                first = False
    print(";")


def mysql_quote(x):
    '''
    Quote the string x using MySQL quoting rules. If x is the empty string,
    return "NULL". Probably not safe against maliciously formed strings, but
    whatever; our input is fixed and from a basically trustable source..
    '''
    if not x:
        return "NULL"
    x = x.replace("\\", "\\\\")
    x = x.replace("'", "''")
    x = x.replace("\n", "\\n")
    return "'{}'".format(x)


if __name__ == "__main__":
    main()
