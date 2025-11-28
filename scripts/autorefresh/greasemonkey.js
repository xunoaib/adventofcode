// ==UserScript==
// @name         WebSocket Refresh Listener
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Refreshes the page when a signal is received from the WebSocket server
// @author       Collin Simpson
// @match        https://adventofcode.com/*/day/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    const ws = new WebSocket("ws://localhost:8765"); // Replace with your WebSocket server's URL

    ws.onopen = function() {
        console.log("Connected to WebSocket server.");
    };

    ws.onmessage = function(event) {
        if (event.data === "refresh") {
          console.log("Received 'refresh' signal. Refreshing page...");
          location.reload();
          
          // scroll part 2 into view
          const part2 = document.getElementById("part2");
          if (part2) {
              part2.scrollIntoView();
          }
        }
    };

    ws.onerror = function(error) {
        console.error("WebSocket error:", error);
    };

    ws.onclose = function() {
        console.log("WebSocket connection closed.");
    };
})();

