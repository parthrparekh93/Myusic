# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 02:12:53 2016

@author: Rohan Kulkarni
@email : rohan.kulkarni@columbia.edu

"""
from flask import Flask,render_template,request
import pickle
import operator

clusters = pickle.load(open("../clusters.p", "rb"))
app = Flask(__name__,static_url_path='/static')

@app.route('/')
def displayWordCloud():

    #frequency_list = [{"text":"study","size":40},{"text":"motion","size":15},{"text":"forces","size":10},{"text":"electricity","size":15},{"text":"movement","size":10},{"text":"relation","size":5},{"text":"things","size":10},{"text":"force","size":5},{"text":"ad","size":5},{"text":"energy","size":85},{"text":"living","size":5},{"text":"nonliving","size":5},{"text":"laws","size":15},{"text":"speed","size":45},{"text":"velocity","size":30},{"text":"define","size":5},{"text":"constraints","size":5},{"text":"universe","size":10},{"text":"physics","size":120},{"text":"describing","size":5},{"text":"matter","size":90},{"text":"physics-the","size":5},{"text":"world","size":10},{"text":"works","size":10},{"text":"science","size":70},{"text":"interactions","size":30},{"text":"studies","size":5},{"text":"properties","size":45},{"text":"nature","size":40},{"text":"branch","size":30},{"text":"concerned","size":25},{"text":"source","size":40},{"text":"google","size":10},{"text":"defintions","size":5},{"text":"two","size":15},{"text":"grouped","size":15},{"text":"traditional","size":15},{"text":"fields","size":15},{"text":"acoustics","size":15},{"text":"optics","size":15},{"text":"mechanics","size":20},{"text":"thermodynamics","size":15},{"text":"electromagnetism","size":15},{"text":"modern","size":15},{"text":"extensions","size":15},{"text":"thefreedictionary","size":15},{"text":"interaction","size":15},{"text":"org","size":25},{"text":"answers","size":5},{"text":"natural","size":15},{"text":"objects","size":5},{"text":"treats","size":10},{"text":"acting","size":5},{"text":"department","size":5},{"text":"gravitation","size":5},{"text":"heat","size":10},{"text":"light","size":10},{"text":"magnetism","size":10},{"text":"modify","size":5},{"text":"general","size":10},{"text":"bodies","size":5},{"text":"philosophy","size":5},{"text":"brainyquote","size":5},{"text":"words","size":5},{"text":"ph","size":5},{"text":"html","size":5},{"text":"lrl","size":5},{"text":"zgzmeylfwuy","size":5},{"text":"subject","size":5},{"text":"distinguished","size":5},{"text":"chemistry","size":5},{"text":"biology","size":5},{"text":"includes","size":5},{"text":"radiation","size":5},{"text":"sound","size":5},{"text":"structure","size":5},{"text":"atoms","size":5},{"text":"including","size":10},{"text":"atomic","size":10},{"text":"nuclear","size":10},{"text":"cryogenics","size":10},{"text":"solid-state","size":10},{"text":"particle","size":10},{"text":"plasma","size":10},{"text":"deals","size":5},{"text":"merriam-webster","size":5},{"text":"dictionary","size":10},{"text":"analysis","size":5},{"text":"conducted","size":5},{"text":"order","size":5},{"text":"understand","size":5},{"text":"behaves","size":5},{"text":"en","size":5},{"text":"wikipedia","size":5},{"text":"wiki","size":5},{"text":"physics-","size":5},{"text":"physical","size":5},{"text":"behaviour","size":5},{"text":"collinsdictionary","size":5},{"text":"english","size":5},{"text":"time","size":35},{"text":"distance","size":35},{"text":"wheels","size":5},{"text":"revelations","size":5},{"text":"minute","size":5},{"text":"acceleration","size":20},{"text":"torque","size":5},{"text":"wheel","size":5},{"text":"rotations","size":5},{"text":"resistance","size":5},{"text":"momentum","size":5},{"text":"measure","size":10},{"text":"direction","size":10},{"text":"car","size":5},{"text":"add","size":5},{"text":"traveled","size":5},{"text":"weight","size":5},{"text":"electrical","size":5},{"text":"power","size":5}];
    frequency_list = []
    for i in xrange(len(clusters)):
        cloud_dict = dict()
        cloud_dict['text'] = clusters[i]['Topic']
        cloud_dict['size'] = clusters[i]['Weight']/2
        frequency_list.append(cloud_dict)
    print(frequency_list)
    return render_template('homepage.html',frequency_list=frequency_list)

@app.route('/results_on_lyrics', methods=['POST'])
def getSimilarSongsGivenLyrics():
    lyrics = request.form['song_lyrics']
    lyrics = lyrics.strip().lower()
    lyrics_set = set(lyrics.split(' '))
    lyrics_array = list(lyrics_set)
    cluster_score_result = [0,0]
    # Get the cluster number
    for i, cluster in enumerate(clusters):
        score = 0
        for lyrics_word in lyrics_array:
            if lyrics_word in cluster['Words']:
                score += 1
        if score > cluster_score_result[1]:
            cluster_score_result[1] = score
            cluster_score_result[0] = i

    cluster_number = cluster_score_result[0]
    print("Cluster number: "+str(cluster_number))
    song_score = []
    for filename in clusters[cluster_number]['Songs']:
        with open('../Songs/'+filename, 'r') as f:
            song_data = f.read()
            f.close()
        song_data_set = set(song_data.strip().lower().split(' '))
        score = len(lyrics_set.intersection(song_data_set))
        song_score.append((filename, score))

    result = sorted(song_score, key=operator.itemgetter(1))[-10:]
    result.reverse()

    return_dict = dict()
    song_list = []
    for filename in result:
        each_song = dict()
        name = filename[0]
        with open('../Songs/'+name, 'r') as f:
            lyrics = f.read()
            f.close()
        each_song['name'] = name
        each_song['lyrics'] = lyrics
        song_list.append(each_song)
    return_dict['song_list'] = song_list

    return render_template("homepage.html", **return_dict)

@app.route('/results_on_name', methods=['POST'])
def getSimilarSongsGivenFile():
    filename = request.form['song_name']
    with open('../Songs/'+filename, 'r') as f:
        filename_data = f.read()
        f.close()
    filename_data_set = set(filename_data.strip().lower().split(' '))

    for i,cluster in enumerate(clusters):
        if filename in cluster['Songs']:
            cluster_number = i
            break

    print("Cluster number: "+str(cluster_number))

    song_score = []
    for filename1 in clusters[cluster_number]['Songs']:
        if filename1 == filename:
            continue
        with open('../Songs/'+filename1, 'r') as f:
            song_data = f.read()
            f.close()
        song_data_set = set(song_data.strip().lower().split(' '))
        score = len(filename_data_set.intersection(song_data_set))
        song_score.append((filename1, score))

    result = sorted(song_score, key=operator.itemgetter(1))[-10:]
    result.reverse()

    return_dict = dict()
    song_list = []
    for filename in result:
        each_song = dict()
        name = filename[0]
        with open('../Songs/'+name, 'r') as f:
            lyrics = f.read()
            f.close()
        each_song['name'] = name
        each_song['lyrics'] = lyrics
        song_list.append(each_song)
    return_dict['song_list'] = song_list

    return render_template("homepage.html", **return_dict)

@app.route('/clusterSongs', methods=['GET'])
def getSongsGivenCluster():
    word_input_set = set('like,got,new'.split(','))
    for i, cluster in enumerate(clusters):
        cluster_set = set(cluster['Words'])
        if word_input_set.intersection(cluster_set) == word_input_set:
            cluster_number = i
            break

    print("Cluster number: "+str(cluster_number))

    result = clusters[cluster_number]['Songs'][:10]

    return_dict = dict()
    song_list = []
    for name in result:
        each_song = dict()
        with open('../Songs/'+name, 'r') as f:
            lyrics = f.read()
            f.close()
        each_song['name'] = name
        each_song['lyrics'] = lyrics
        song_list.append(each_song)
    return_dict['song_list'] = song_list

    return render_template("homepage.html", return_dict=return_dict)


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost',port=8075)
