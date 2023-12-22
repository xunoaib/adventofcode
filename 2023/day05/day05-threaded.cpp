// Multithreaded version of Part 2 which runs in 36 seconds on my hardware

#include <iostream>
#include <limits>
#include <mutex>
#include <queue>
#include <random>
#include <sstream>
#include <thread>
#include <tuple>
#include <utility>
#include <vector>
using namespace ::std;

using RangeTuple = pair<long long, long long>;
using MapTuple = tuple<long long, long long, long long>;

auto parse_seeds(istream &in) {
    string line;
    getline(in, line);
    stringstream ss(line);
    getline(in, line);
    ss >> line;
    vector<long long> seeds;
    while (ss >> line) {
        seeds.push_back(stol(line));
    }
    return seeds;
}

auto parse_maps(istream &in) {
    string line;
    vector<vector<MapTuple>> maps;
    while (getline(in, line)) {
        auto m = vector<MapTuple>();
        while (getline(in, line) && line.length()) {
            stringstream ss(line);
            long long dst, start, length;
            ss >> dst >> start >> length;
            m.push_back({dst, start, start + length});
        }
        maps.push_back(m);
    }
    return maps;
}

// Split large ranges into smaller fixed-size groups
auto split_ranges(vector<long long> &seeds, long long amount = 40000000) {
    vector<RangeTuple> ranges;
    for (size_t i = 0; i < seeds.size(); i += 2) {
        auto start = seeds[i];
        auto length = seeds[i + 1];
        while (length > amount) {
            ranges.push_back({start, amount});
            start += amount;
            length -= amount;
        }
        ranges.push_back({start, length});
    }
    return ranges;
}

// Function to process a range and return the minimum value
auto processRange(vector<vector<MapTuple>> &maps, queue<RangeTuple> &rangeQueue,
                  mutex &queueMutex) {
    long long minResult = numeric_limits<long long>::max();

    while (true) {
        unique_lock<mutex> lock(queueMutex);
        if (rangeQueue.empty()) {
            return minResult;
        }

        RangeTuple range = rangeQueue.front();
        rangeQueue.pop();
        lock.unlock();

        // cout << "processing: " << range.first << " > " << range.second << endl;
        for (auto j = range.first; j < range.first + range.second; j++) {
            auto res = j;
            for (auto &m : maps) {
                for (const auto [dst, src, end] : m) {
                    if (src <= res && res < end) {
                        res = res - src + dst;
                        break;
                    }
                }
            }
            minResult = min(minResult, res);
        }
    }
}

int main() {
    auto seeds = parse_seeds(cin);
    auto maps = parse_maps(cin);
    auto ranges = split_ranges(seeds);

    queue<RangeTuple> rangeQueue;
    mutex queueMutex;

    for (const auto &range : ranges) {
        rangeQueue.push(range);
    }

    const int numThreads = 8;
    vector<thread> threads;
    cout << "Number of threads: " << numThreads << endl;

    vector<long long> threadResults(numThreads,
                                    numeric_limits<long long>::max());

    // Create threads and assign work from the queue
    for (int i = 0; i < numThreads; ++i) {
        threads.emplace_back(
            [i, &rangeQueue, &queueMutex, &threadResults, &maps]() {
                threadResults[i] = processRange(maps, rangeQueue, queueMutex);
            });
    }

    // Join the threads
    for (auto &thread : threads) {
        thread.join();
    }

    // Find the overall minimum result from individual thread results
    long long overallMinResult = numeric_limits<long long>::max();
    for (long long result : threadResults) {
        if (result < overallMinResult) {
            overallMinResult = result;
        }
    }

    cout << "Overall minimum result: " << overallMinResult << endl;
    return 0;
}
