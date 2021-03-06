#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import re

SITE_IDENTIFIER = 'full_stream_net'
SITE_NAME = 'Full-Stream.net'
SITE_DESC = 'Film et Série en Streaming HD - Vk.Com - Netu.tv - ExaShare - YouWatch'

URL_MAIN = 'http://full-stream.net'
MOVIE_NEWS = 'http://full-stream.net/lastnews/'
MOVIE_VIEWS = 'http://full-stream.net/films-en-vk-streaming/'
MOVIE_GENRES = True
SERIE_SERIES = 'http://full-stream.net/seriestv/'
SERIE_VFS = 'http://full-stream.net/seriestv/vf/'
SERIE_VOSTFRS = 'http://full-stream.net/seriestv/vostfr/'

def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Nouveautés', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les plus vues', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genre', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries VF', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries VOSTFR', 'series.png', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            #sSearchText = cUtil().urlEncode(sSearchText)
            sUrl = 'http://full-stream.net/xfsearch/'+sSearchText+'/'  
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return  
    
    
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['HD/HQ','http://full-stream.net/films-en-vk-streaming/haute-qualite/'] )
    liste.append( ['Action','http://full-stream.net/films-en-vk-streaming/action/'] )
    liste.append( ['Aventure','http://full-stream.net/films-en-vk-streaming/aventure/'] )
    liste.append( ['Animation','http://full-stream.net/films-en-vk-streaming/animation/'] )
    liste.append( ['Arts Martiaux','http://full-stream.net/films-en-vk-streaming/arts-martiaux/'] )
    liste.append( ['Biopic','http://full-stream.net/films-en-vk-streaming/biopic/'] )
    liste.append( ['Comedie','http://full-stream.net/films-en-vk-streaming/comedie/'] )
    liste.append( ['Comedie Dramatique','http://full-stream.net/films-en-vk-streaming/comedie-dramatique/'] )
    liste.append( ['Comedie Musicale','http://full-stream.net/films-en-vk-streaming/comedie-musicale/'] )
    liste.append( ['Drame','http://full-stream.net/films-en-vk-streaming/drame/'] )
    liste.append( ['Documentaire','http://full-stream.net/films-en-vk-streaming/documentaire/'] ) 
    liste.append( ['Horreur','http://full-stream.net/films-en-vk-streaming/horreur/'] )
    liste.append( ['Fantastique','http://full-stream.net/films-en-vk-streaming/fantastique/'] )
    liste.append( ['Guerre','http://full-stream.net/films-en-vk-streaming/guerre/'] )
    liste.append( ['Policier','http://full-stream.net/films-en-vk-streaming/policier/'] )
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 
    

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('&amp;w=210&amp;h=280','')
    sPattern = 'full-stream-view-hover"><img src=".+?src=(.+?)" alt="(.+?)".+?<h2><a href="(.+?)">.+?</a></h2>.+?<b>Résumé</b>(.+?)</div>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))
            if '/seriestv/' in sUrl  or 'saison' in aEntry[2]:
                oGui.addTV(SITE_IDENTIFIER, 'serieHosters', aEntry[1], '', aEntry[0], aEntry[3], oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', aEntry[1], '', aEntry[0], aEntry[3], oOutputParameterHandler)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<div class="navigation".+? <span.+? <a href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False
    

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();


    sPattern = '<iframe src="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)                   
        
            if (oHoster != False):         
                try:
                    oHoster.setHD(sHosterUrl)
                except: pass
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)

                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 

    oGui.setEndOfDirectory()
    
def serieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<a href="([^<]+)" title="([^<]+)" target="seriePlayer" class="ilink sinactive">'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sHosterUrl = str(aEntry[0])
            oHoster = cHosterGui().checkHoster(sHosterUrl)
        
            if (oHoster != False):
                sTitle = aEntry[1]
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)    

    oGui.setEndOfDirectory()