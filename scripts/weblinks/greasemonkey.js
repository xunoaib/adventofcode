// ==UserScript==
// @name         Advent of Code: Quick Links
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Adds links to the "Private Leaderboard" and "My Times" pages
// @author       Collin Simpson
// @match        https://adventofcode.com/*
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    const leaderboard_id = 1126771; // modify as needed

    const xpath = "/html/body/header/div[2]/nav/ul";
    const result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
    const ul = result.singleNodeValue;

    if (ul) {
        const currentUrl = window.location.href;
        const yearMatch = currentUrl.match(/https:\/\/adventofcode\.com\/(\d+)\//);

        if (yearMatch && yearMatch[1]) {
            const year = yearMatch[1];
            const leaderboardUrl = `https://adventofcode.com/${year}/leaderboard/private/view/${leaderboard_id}`;
            const personalTimesUrl = `https://adventofcode.com/${year}/leaderboard/self`;

            const createLinkItem = (url, text) => {
                const li = document.createElement('li');
                const link = document.createElement('a');
                link.href = url;
                link.textContent = text;
                link.rel = 'noopener noreferrer';
                li.appendChild(link);
                return li;
            };

            const privateLeaderboardLi = createLinkItem(leaderboardUrl, '[Private LB]');
            const personalTimesLi = createLinkItem(personalTimesUrl, '[My Times]');

            ul.appendChild(privateLeaderboardLi);
            ul.appendChild(personalTimesLi);
        }
    }
})();
