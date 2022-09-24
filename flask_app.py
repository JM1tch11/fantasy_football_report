import pandas as pd
import numpy as np
import io
from IPython.core.display import display, HTML
from flask import Flask, render_template, request, redirect, url_for
import requests
from all_functions import load_data, get_params
from league_analyzer import power_table, get_wins_vs_lg, get_sched_switch, get_eff, team_efficiency
# =============================================================================
# from week_simulation import headings_bets, data_bets, tstamp
# from season_simulation import headings_w, data_w, headings_r, data_r, headings_p, data_p, headings_s, data_s
# from data_setup import headings_st, data_st, headings_pr, data_pr, rank_data, headings_scen, data_scen, headings2_scen, data2_scen, eff_plot2, pos_plot2
# =============================================================================
from records import headings_rec, data_rec
import json
from flask_fontawesome import FontAwesome
from IPython.core.display import display, HTML

league_id = 791545
season = 2022
swid = "{196DA414-D50C-4582-AE60-ED4D42FDF07A}"
espn = "AEBi3NIMa0rd29d99v48uQ4lu7P1Ust1PdDWyA3653RtuVXWrEYdCOK5HnFBMSdwUtAQPgHOXDexUA%2F45%2BEb4H4GBNumz5iHcn41KTmt3PJoisqKLqmGnFEfDNF7gqVKpKCSahHMoXY%2Bw8aPzzbYYz0%2FNG1hTVvZn4AprZpBxSdDr98ZcW5ZBe7bzojSyJpjN%2BI%2F7855S2sOaIrZ1B8Ov9Df9CylwpToQy5TsYYECJDu6YHl3%2B9YHasZrAPpEDSo2wR0HhP%2FWZzsK9m9bLVC8uSYq0RvtKpGe%2FlGInjZoI2ehUa%2Fthj0or0DJNSnCLcRGP8%3D"

d = load_data(league_id, season, swid, espn)
week = np.where(get_params(d)["current_week"] > get_params(d)["regular_season_end"],
                "Final " + str(season),
                "Week " + str(get_params(d)["current_week"]))
week = week.item(0)

# create flask app
app = Flask(__name__)
fa = FontAwesome(app)


###########################
# Flask routes
##########################
@app.route("/")
def home():
    return render_template("powerrank.html",
                           headings_st=headings_st, data_st=data_st,
                           headings_pr=headings_pr, data_pr=data_pr,
                           week=week, rank_data=rank_data)


@app.route("/simulations/")
def sims():
    return render_template("simulations.html", headings_bets=headings_bets, data_bets=data_bets,
                           headings_w=headings_w, data_w=data_w,
                           headings_r=headings_r, data_r=data_r,
                           headings_s=headings_s, data_s=data_s,
                           headings_p=headings_p, data_p=data_p,
                           week=week, tstamp=tstamp)


@app.route("/scenarios/")
def scen():
    return render_template("scenarios.html", headings_scen=headings_scen, data_scen=data_scen,
                           headings2_scen=headings2_scen, data2_scen=data2_scen)


@app.route("/efficiency/")
def eff():
    return render_template("efficiencies.html", eff_plot=eff_plot2, pos_plot=pos_plot2)


@app.route("/champions/")
def champs():
    champs = pd.read_csv(
        r"C:\Users\hirsh\OneDrive\Desktop\Data Science Stuff\Projects\FF Leagues\FF Analysis\Flask_Cool\tables\champions.csv")
    champs["Count"] = champs.groupby("Champion").cumcount() + 1
    champs = champs.assign(Icon=champs["Count"].apply(lambda n: n * '<span class="fab fa-trophy"></span>'))
    prev_champs = champs[["Season", "Champion"]]
    champ_count = champs.drop_duplicates(subset="Champion", keep="last").sort_values(["Count", "Season"],
                                                                                     ascending=False).drop("Season",
                                                                                                           axis=1)

    headings_pc = tuple(prev_champs.columns)
    data_pc = [tuple(x) for x in prev_champs.to_numpy()]

    headings_cc = tuple(champ_count.columns)
    data_cc = [tuple(x) for x in champ_count.to_numpy()]

    return render_template("champions.html", headings_pc=headings_pc, data_pc=data_pc,
                           headings_cc=headings_cc, data_cc=data_cc,
                           champs=champs)


@app.route("/records/")
def records():
    return render_template("records.html", headings_rec=headings_rec, data_rec=data_rec)


# Run app
if __name__ == "__main__":
    app.run()
