from selenium import webdriver
from flask import Flask, render_template,request
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

app = Flask(__name__)

# headless mode
chrome_options = Options()
chrome_options.add_argument('--headless')

def find_hashtags(countryname):
    driver = webdriver.Chrome(options=chrome_options)
    # https: // www.exportdata.io / trends /
    driver.get(f"https://twitter-trends.iamrohit.in/{countryname}")
    topic=''
    try:

        topic_name = driver.find_elements(By.XPATH, "//table[@id='twitter-trends']/tbody/tr[1]/th[3]")
        topic = [element.text.strip() for element in topic_name  if element.text.strip()]
        tweet_volume_elements = driver.find_elements(By.XPATH, "//table[@id='twitter-trends']/tbody/tr[1]/th[2]")
        tweet_volume = [element.text.strip() for element in tweet_volume_elements  if element.text.strip()]
    except Exception as e:
        print("Error",e)
        tweet_volume = ["Tweet count not found"]
    driver.quit()
    return tweet_volume, topic


@app.route("/",methods =["POST","GET"])
def find_trending_hashtags_by_country_name():
    if request.method == "POST":
        get_country_name =  request.form['sc']
        total_volume = find_hashtags(get_country_name)
        return render_template("trending.html",get_country_name = get_country_name, total_volume=total_volume)
    else:
        get_country_name = "Can't find Hashtags"
        return render_template("trending.html",unable_to_find= get_country_name)


if __name__ == "__main__":
    app.run(debug=True)