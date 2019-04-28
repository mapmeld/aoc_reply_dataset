// ==UserScript==
// @name         AOC Reply Set
// @version      0.1
// @description  scan Twitter replies
// @author       You
// @match       *://twitter.com/*
// @match       *://*.twitter.com/*
// @grant none
// ==/UserScript==

(function() {
    'use strict';
    console.log('scan functions are available');

    // Your code here...
    window.scanaoc = function () {
       // open up whole thread
      $('.ThreadedConversation-moreRepliesLink').trigger('click');

      setTimeout(() => {
        let records = [];

        let tweets = $('.PermalinkOverlay-modal .tweet');
        let originTweet = $(tweets.get(0));
          let originTweetID = originTweet.attr('data-tweet-id');
          let originTweetTime = originTweet.find('.metadata').text().trim();
          let originTweeter = originTweet.attr('data-name');
          let originTweeterSN = originTweet.attr('data-screen-name');
          let tweetTexts = originTweet.find('.tweet-text');
          let originText = $(tweetTexts.get(0)).text().replace('http', ' http').replace('pic.twitter', ' pic.twitter');
          let quoteTweetText = tweetTexts.length > 1 ? ($(tweetTexts.get(1)).text().replace('http', ' http').replace('pic.twitter', ' pic.twitter')) : '';
          let quoteTweetUser = tweetTexts.length > 1 ? originTweet.find('.QuoteTweet-innerContainer').attr('data-screen-name') : '';
          let originVerified = originTweet.hasClass('with-social-proof');
          let favs = $(originTweet.find('.js-actionFavorite .ProfileTweet-actionCount').get(0));
          favs = (favs.attr('data-tweet-stat-count') || favs.text()).trim()
          let rts = $(originTweet.find('.js-actionRetweet .ProfileTweet-actionCount').get(0));
          rts = (rts.attr('data-tweet-stat-count') || rts.text()).trim()
         let originalData = [originTweetID, originTweetTime, originTweeter, originTweeterSN, originVerified, originText, quoteTweetUser, quoteTweetText, favs, rts];

        for (let i = 1; i < tweets.length; i++) {
           let record = [];
           let tweet = $(tweets.get(i));
           record.push( tweet.attr('data-tweet-id') );
           record.push( tweet.attr('data-conversation-id') );
           record.push( tweet.find('._timestamp').attr('data-time') );
           record.push( tweet.attr('data-name') );
           record.push( tweet.attr('data-screen-name') );
           record.push( tweet.hasClass('with-social-proof') );
           record.push( tweet.attr('data-mentions') );
           record.push( tweet.attr('data-has-cards') || false );
           let replyTexts = tweet.find('.tweet-text');
           record.push( $(replyTexts.get(0)).text().replace('http', ' http').replace('pic.twitter', ' pic.twitter') );
           record.push( $(replyTexts.get(0)).attr('lang') );

           // quote tweet
           //record.push(replyTexts.length > 1 ? tweet.find('.QuoteTweet-innerContainer').attr('data-screen-name') : '');
           //record.push(replyTexts.length > 1 ? $(replyTexts.get(1)).text().replace('http', ' http') : '');

           let links = tweet.find('.tweet-text a');
           let mylinks = [];
           for (var lk = 0; lk < links.length; lk++) {
               mylinks.push( $(links.get(lk)).attr('href') );
           }
           record.push( mylinks.join(' ') );


           let favs = $(tweet.find('.js-actionFavorite .ProfileTweet-actionCount').get(0));
          favs = (favs.attr('data-tweet-stat-count') || favs.text()).trim()
          let rts = $(tweet.find('.js-actionRetweet .ProfileTweet-actionCount').get(0));
          rts = (rts.attr('data-tweet-stat-count') || rts.text()).trim()
            record.push(favs);
            record.push(rts);

           records.push(record);
           //GM.setValue(tweet.attr('data-tweet-id'), JSON.stringify(record));
        }
        let file = JSON.stringify({ origin: originalData, replies: records });
        var a = document.createElement('a');
        a.href = 'data:application/json;charset=utf-8,' + encodeURIComponent(file);
        //supported by chrome 14+ and firefox 20+
        a.download = originTweetID + '.json';
        //needed for firefox
        document.getElementsByTagName('body')[0].appendChild(a);
        //supported by chrome 20+ and firefox 5+
        a.click();
      }, 750);
    };
})();
