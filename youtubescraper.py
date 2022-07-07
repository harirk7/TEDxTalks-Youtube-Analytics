def get_channels_stats(youtube, channels_id):
    """
    Get channels stats

    Parameters:
        youtube: build object of Youtube API
        channel_ids: list of Youtube channel IDs
    
    Returns:
        all channel stats for each channel ID
    """

    channels_data = []

    request = youtube.channels().list(
        part= "snippet,contentDetails,statistics",
        id=','.join(channels_id)
    )
    response = request.execute()

    #loop through items
    for i in range(len(response['items'])):
        data = {
            'channel_name': response['items'][i]['snippet']['title'],
            'subscribers': response['items'][i]['statistics']['subscriberCount'],
            'videos': response['items'][i]['statistics']['videoCount'],
            'views': response['items'][i]['statistics']['viewCount'],
            'playlist_id': response['items'][i]['contentDetails']['relatedPlaylists']['uploads']
        }

        channels_data.append(data)
    
    return channels_data



def get_playlists_id(channels_stats):
    playlists_id = []
    
    for i in range(len(channels_stats)):
        playlist_id = channels_stats.loc[:, 'playlist_id'].iloc[i]
        playlists_id.append(playlist_id)
    
    return playlists_id



def get_videos_id(youtube, playlists_id):
    """
    Get video ids

    Parameters:
        youtube: build object of Youtube API
        playlist_ids: list of Youtube channel playlist IDs
    
    Returns:
        all video IDs for each channel playlist ID
    """

    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId = ','.join(playlists_id),
        maxResults = 50
    )
    response = request.execute()

    videos_id = []
    for i in range(len(response['items'])):
        video_id = response['items'][i]['contentDetails']['videoId']
        videos_id.append(video_id)
    
    next_page_token = response.get('nextPageToken')

    while next_page_token is not None:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId = ','.join(playlists_id),
            maxResults = 50,
            pageToken = next_page_token
        )
        response = request.execute()

        for i in range(len(response['items'])):
            video_id = response['items'][i]['contentDetails']['videoId']
            videos_id.append(video_id)
        
        next_page_token = response.get('nextPageToken')

    return videos_id



def get_videos_details(youtube, video_ids):
    """
    Get video details

    Parameters:
        youtube: build object of Youtube API
        video_ids: list of Youtube channel video IDs
    
    Returns:
        all video details [id, title, description, published date, tags, language,
            duration, views, likes, comments, favorites] for each channel playlist ID
    """
    videos_data = []
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute()

        for video in response['items']:
            data = {
                'video_id': video['id'],
                'channel_title': video['snippet']['channelTitle'],
                'video_title': video['snippet']['title'],
                'description': video['snippet'].get('description'),
                'published_date': video['snippet']['publishedAt'],
                'tags': video['snippet'].get('tags'),
                'language': video['snippet'].get('defaultAudioLanguage'),
                'duration': video['contentDetails']['duration'],
                'views': video['statistics'].get('viewCount'),
                'likes': video['statistics'].get('likeCount'),
                'comments': video['statistics'].get('commentCount'),
                'favorites': video['statistics'].get('favoriteCount')
            }
            videos_data.append(data)

    return videos_data



def get_video_comments(youtube, videos_id):
  
    # retrieve youtube video results
    request = youtube.commentThreads().list(
        part = "id, snippet, replies",
        videoId = videos_id,
        maxResults = 20,
        order = 'relevance'
    )
    
    response = request.execute()

    # comments = []
    replies = []
    while response:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay'],
            replycount = item['snippet']['totalReplyCount']

            if replycount>0:
                for reply in item['replies']['comments']:
                    reply = reply['snippet']['textDisplay']
                    replies.append(reply)
        
        if 'nextPageToken' in response:
            request = youtube.commentThreads().list(
                part = "id, snippet, replies",
                videoId = 'LGKT_m8D5EM',
                maxResults = 20,
                order = 'relevance'
            )
            response = request.execute()
            
    return replies