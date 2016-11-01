from __future__ import print_function
import requests
import logging
#
base_url = 'https://gateway-a.watsonplatform.net/calls'
logger = logging.getLogger(__name__)
#
def _check_request_for_error(r):
    json_format = r.json()
    if json_format['status'] == 'ERROR':
        return json_format['statusInfo']
    #
    return None
#
def get_taxonomy_from_text(text, apikey):
    params = {
        'text': text,
        'outputMode': 'json',
        'apikey': apikey,
    }
    r = requests.get(base_url+'/text/TextGetRankedTaxonomy', params=params)
    error = _check_request_for_error(r)
    if error is not None:
        logger.error('There was an error with the request. Error:\n%s', r.text)
        raise Exception('An error was returned from the API request: '+str(error))
    #
    '''
    Example response:

    {
        "status": "OK",
        "usage": "By accessing AlchemyAPI or using information generated by AlchemyAPI, you are agreeing to be bound by the AlchemyAPI Terms of Use: http://www.alchemyapi.com/company/terms.html",
        "totalTransactions": "1",
        "language": "english",
        "taxonomy": [
            {
                "confident": "no",
                "label": "/technology and computing/consumer electronics/telephones/mobile phones/smart phones",
                "score": "0.309155"
            },
            {
                "confident": "no",
                "label": "/technology and computing/consumer electronics/portable entertainment",
                "score": "0.25882"
            },
            {
                "confident": "no",
                "label": "/technology and computing/operating systems",
                "score": "0.182776"
            }
        ]
    }
    '''
    #
    try:
        taxonomy = r.json()['taxonomy']
        return {x['label']:{'taxonomy':x['score'], 'confident':x['confident']} for x in taxonomy}
    except:
        logger.exception('Could not parse the keywords from the result:\n%s', r.text)
        raise Exception('Could not parse the keywords from the result:\n'+str(r.text))
    #
#
def get_keywords_from_text(text, apikey, get_sentiment=False, get_knowledge_graph=False):
    '''
    Note: Setting 'get_sentiment' or 'get_knowledge_graph' to True will use extra API calls.
    '''
    #
    params = {
        'text': text,
        'outputMode': 'json',
        'sentiment': int(get_sentiment),
        'knowledgeGraph': int(get_knowledge_graph),
        'apikey': apikey,
    }
    r = requests.get(base_url+'/text/TextGetRankedKeywords', params=params)
    error = _check_request_for_error(r)
    if error is not None:
        logger.error('There was an error with the request. Error:\n%s', r.text)
        raise Exception('An error was returned from the API request: '+str(error))
    #
    '''
    Example response:

    {
        "status": "OK",
        "usage": "By accessing AlchemyAPI or using information generated by AlchemyAPI, you are agreeing to be bound by the AlchemyAPI Terms of Use: http://www.alchemyapi.com/company/terms.html",
        "totalTransactions": "3",
        "language": "english",
        "keywords": [
            {
                "knowledgeGraph": {
                    "typeHierarchy": "/devices/mobile devices/smartphones/iphone"
                },
                "relevance": "0.90671",
                "sentiment": {
                    "score": "0.737375",
                    "type": "positive"
                },
                "text": "iPhone"
            },
            {
                "knowledgeGraph": {
                    "typeHierarchy": "/products/images"
                },
                "relevance": "0.549369",
                "sentiment": {
                    "score": "0.737375",
                    "type": "positive"
                },
                "text": "Images"
            }
        ]
    }
    '''
    #
    try:
        keywords = r.json()['keywords']
        for x in keywords:
            x['relevance'] = float(x['relevance'])
            #
            if 'sentiment' in x:
                if 'score' not in x['sentiment'] and x['sentiment']['type'] == 'neutral':
                    x['sentiment']['score'] = 0
                #
                x['sentiment']['score'] = float(x['sentiment']['score'])
            else:
                x['sentiment'] = {}
                x['sentiment']['score'] = None
            #
            if 'knowledgeGraph' not in x:
                x['knowledgeGraph'] = {}
                x['knowledgeGraph']['typeHierarchy'] = None
            #
        #
        return {x['text']:{'relevance':x['relevance'], 'sentiment':x['sentiment']['score'], 'knowledge_graph':x['knowledgeGraph']['typeHierarchy']} for x in keywords}
    except:
        logger.exception('Could not parse the keywords from the result:\n%s', r.text)
        raise Exception('Could not parse the keywords from the result:\n'+str(r.text))
    #
#
def get_sentiment_score_from_text(text, apikey):
    params = {
        'text': text,
        'outputMode': 'json',
        'apikey': apikey,

        'apikey': "3b5857fc266a2b7b5fca6a661e72570c6dc3f8a2"

    }
    r = requests.get(base_url+'/text/TextGetTextSentiment', params=params)
    error = _check_request_for_error(r)
    if error is not None:
        logger.error('There was an error with the request. Error:\n%s', r.text)
        raise Exception('An error was returned from the API request: '+str(error))
    #
    '''
    Example response:

    {
        "status": "OK",
        "usage": "By accessing AlchemyAPI or using information generated by AlchemyAPI, you are agreeing to be bound by the AlchemyAPI Terms of Use: http://www.alchemyapi.com/company/terms.html",
        "totalTransactions": "1",
        "language": "english",
        "docSentiment": {
            "score": "0.688812",
            "type": "positive"
        }
    }
    '''
    #
    try:
        return float(r.json()['docSentiment']['score'])
    except:
        logger.exception('Could not parse the keywords from the result:\n%s', r.text)
        raise Exception('Could not parse the sentiment score from the result:\n'+str(r.text))
    #
#
def get_sentiment_score_for_targets_from_text(text, targets, apikey):
    params = {
        'text': text,
        'targets': targets,
        'outputMode': 'json',
        'apikey': apikey,
    }
    r = requests.get(base_url+'/text/TextGetTargetedSentiment', params=params)
    error = _check_request_for_error(r)
    if error is not None:
        logger.error('There was an error with the request. Error:\n%s', r.text)
        raise Exception('An error was returned from the API request: '+str(error))
    #
    '''
    Example response:

    {
        "status": "OK",
        "usage": "By accessing AlchemyAPI or using information generated by AlchemyAPI, you are agreeing to be bound by the AlchemyAPI Terms of Use: http://www.alchemyapi.com/company/terms.html",
        "totalTransactions": "1",
        "language": "english",
        "results": [
            {
                "sentiment": {
                    "type": "neutral"
                },
                "text": "Apple"
            },
            {
                "sentiment": {
                    "score": "-0.81546",
                    "type": "negative"
                },
                "text": "Blackberry"
            }
        ]
    }
    '''
    #
    try:
        results = r.json()['results']
        for x in results:
            if 'score' not in x['sentiment'] and x['sentiment']['type'] == 'neutral':
                x['sentiment']['score'] = 0
            #
            x['sentiment']['score'] = float(x['sentiment']['score'])
        #
        return {x['text']:{'sentiment':x['sentiment']['score']} for x in results}
    except:
        logger.exception('Could not parse the keywords from the result:\n%s', r.text)
        raise Exception('Could not parse the sentiment score from the result:\n'+str(r.text))
    #
#
class ExceptionLogger(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
    #
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        # see here: http://stackoverflow.com/a/16993115/3731982
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        #
        self._logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    #
#
def _install_thread_excepthook():
    '''
    Workaround for sys.excepthook thread bug
    From http://spyced.blogspot.com/2007/06/workaround-for-sysexcepthook-bug.html (https://sourceforge.net/tracker/?func=detail&atid=105470&aid=1230540&group_id=5470).
    Call once from __main__ before creating any threads.
    If using psyco, call psyco.cannotcompile(threading.Thread.run)
    since this replaces a new-style class method.
    '''
    import threading
    init_old = threading.Thread.__init__
    def init(self, *args, **kwargs):
        init_old(self, *args, **kwargs)
        run_old = self.run
        def run_with_except_hook(*args, **kw):
            try:
                run_old(*args, **kw)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                sys.excepthook(*sys.exc_info())
        self.run = run_with_except_hook
    threading.Thread.__init__ = init
#
if __name__ == '__main__':
    import sys
    _install_thread_excepthook()
    sys.excepthook = ExceptionLogger().handle_exception
    #
    ##############
    #
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    #
    import color_stream_handler
    stream_handler = color_stream_handler.ColorStreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(levelname)-6s : %(name)-25s : %(message)s'))
    #file_log_handler = logging.FileHandler('alchemy.log')
    #
    root_logger.addHandler(stream_handler)
    #root_logger.addHandler(file_log_handler)
    #
    logger = logging.getLogger(__name__)
    #
    ##############
    #
    import yaml
    with open('api_keys.yaml', 'r') as f:
        api_keys = yaml.load(f)
    #
    apikey = api_keys['alchemy']['apikey']
    #
    ##############
    #
    #print(get_sentiment_score_from_text('These Images Have Us VERY Excited About The iPhone 7.', apikey))
    #print(get_sentiment_score_for_targets_from_text('These Images Have Us VERY Excited About The iPhone 7', 'iphone', apikey))
    #
    #print(get_taxonomy_from_text('These Images Have Us VERY Excited About The iPhone 7.', apikey))
    #
    #print(get_keywords_from_text('These Images Have Us VERY Excited About The iPhone 7.', apikey, True, True))
    #print(get_keywords_from_text('These Images Have Us VERY Excited About The iPhone 7.', apikey))
    #
    print("Keywords for text \'I did not have to eat that candy apple like that lol\'")
    print(get_keywords_from_text('I did not have to eat that candy apple like that lol', apikey, False, True))
    #print(get_keywords_from_text('I like Apple products.', apikey, False, True))
    #
    #print(get_sentiment_score_from_text('Apple is good. Blackberry is bad.', apikey))
    #print(get_sentiment_score_for_targets_from_text('Apple is good. Blackberry is bad.', 'Apple|Blackberry', apikey))
    #
    '''
    url = "http://www.zacks.com/stock/news/207968/stock-market-news-for-february-19-2016"
    targets = "NASDAQ|Dow"
    r = requests.get('https://gateway-a.watsonplatform.net/calls/url/URLGetTargetedSentiment?url=%s&targets=%s&outputMode=json&apikey=%s'%(url, targets, apikey))
    print(r.status_code)
    print(r.text)
    print(r.encoding)
    print(r.headers['content-type'])
    print(r.json())
    '''
#
