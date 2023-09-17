---
aliases:
- /news/2023-simulating-internet-shutdowns.html
date: 2023-05-04T11:00:00+00:00
title: "Researching Android's behavior during Internet shutdowns"
---

## Background

The Briar team is currently doing some research into the long-term
evolution of the project.
We have two main branches of research, which we refer to as "social mesh"
and "public mesh" respectively.

The social mesh part of our research is concerned with routing
messages within a social graph of established and trusted contacts.
The public mesh part is concerned with routing messages via untrusted
devices. The overarching goal is to find suitable mechanisms and concepts
for improving Briar's messaging capabilities, especially in situations
where Internet access is unavailable, such as during an
Internet shutdown.

## Simulated Internet shutdowns

One aspect of our public mesh research is looking into how Android devices
behave in case of an Internet shutdown.
While it is clear that during a full or partial Internet shutdown, many
websites and services cannot be reached from any device, it is not
so clear which functionality remains intact.
The Android operating system has mechanisms to detect whether
a device has a working Internet connection, and we wanted to find
out whether this assessment might prevent installed apps from communicating
with servers that were technically still reachable.

To get insight into this, we decided to simulate Internet shutdowns on a
wireless network using different techniques, and to observe how Android
devices reacted while connected to that Wi-Fi.

The experiments showed that it is relatively simple to simulate a
partial Internet shutdown where Android thinks the Internet connection is
not working, but this does not seem to prevent any non-blocked Internet
traffic. The operating system and the browser give strong visual
indications to the user that the current Wi-Fi network doesn't provide
Internet access, but the browser
and other apps just keep working nonetheless.

This is good news for apps like Briar that are designed to operate during
Internet shutdowns, making use of whatever network connectivity is
available.

### Experiment setup

The basic setup for our experiments was a Linux-based Wi-Fi router that was
configured in different ways to simulate an Internet shutdown.
A phone running Android 11 was used for testing.
The idea was to block just enough of the network to make Android think the
Internet connection was broken, and then test whether apps could still use
the network.

We already knew that a special domain name was used for checking Internet
connectivity: `connectivitycheck.gstatic.com`.
Android uses this domain to test whether the phone is connected to a Wi-Fi
network with a so-called captive portal, where the user needs to accept
some terms and conditions before gaining Internet access.
We manipulated the DNS server to behave in different ways for that special
domain name and created four distinct situations:

1. Install a fake captive portal reachable at `connectivitycheck.gstatic.com`.
2. No captive portal, instead configure the DNS server to behave irregularly
   for `connectivitycheck.gstatic.com` and some more of Google's domains:
	* a) return unused IP addresses,
	* b) return DNS error responses,
	* c) do not return DNS responses at all.

A combination of `dnsmasq`, `nginx` and `iptables` was used to set up
these situations.

### 1. Fake captive portal

If you've used an Android phone on a public Wi-Fi network,
you're probably familiar with the basic situation created
by setup 1).
Right after establishing a connection to the Wi-Fi, Android shows a
notification telling you that you're required to sign in to the network
in order to use it.
The wireless connections settings screen shows a similar message.
In addition, the Wi-Fi symbol in the status bar has a small "X" in the
corner, as a hint that the network does not provide Internet access.
Tapping the notification opens a browser window that usually displays
the captive portal, prompting you to enter a token or simply accept some
terms and conditions.

We didn't simulate a full-blown captive portal, just returned an unexpected
HTTP response code for the relevant endpoint,
`connectivitycheck.gstatic.com/generate_204`.
Usually, a router would block other network traffic until the user had
completed the required confirmation steps in the captive portal.
In our case, all network traffic was still possible as far as the
router was concerned.
We used the Chrome browser to check network access to other websites.
Even though the browser showed a black bar at the top saying
"No Internet connection", we were able to browse random sites just fine.

### 2. Manipulating DNS responses for some of Google's domains

Setup 2) was different from the first one in that Android was unable to
connect to `connectivitycheck.gstatic.com/generate_204` and receive any HTTP
response at all.

For case a), `dnsmasq` was configured to return a local IP address for that
domain name. We knew this address was not in use at the time, so Android
could not connect to an HTTP server at that address.
For case b), `dnsmasq` was configured to return an NXDOMAIN response
instead, so Android would know immediately that the address lookup had
failed.
For case c), `iptables` was configured to silently drop the relevant
DNS requests.

In all three cases, Android didn't report that the Wi-Fi connection was
broken, in contrast to setup 1).

Inspecting DNS traffic on the network, we were able to observe that other
domains were queried without any user interaction:
`google.com` and `www.google.com`.
Extending the scenarios to block these domains in addition to the
connectivity check _did_ cause Android to report that the the Wi-Fi connection
was broken. The small "X" on the status bar icon appeared, the
Wi-Fi settings screen showed "No Internet" for the current network,
and Chrome had the additional black bar at the top saying "No Internet
connection".

Unlike setup 1), there was no prompt to sign into the network. This makes
sense, as Android was not able to reach the captive portal.

As in the first setup, we used Chrome to check random websites. Except
for Google, which was really blocked in this setup, we had no problems
browsing the web.

### Summary

When an Android device thinks that its Internet
connection doesn't work, either due to a captive portal or due to certain
Google domains being unreachable, apps on the device are still able to
connect to IP addresses that remain reachable, and the device can still
resolve DNS queries for other domains.
Even though various parts of the UI indicate that the system considers the
Wi-Fi connection to be offline, the system does not seem to block any
traffic as a result of this assessment.

For our project, this is good news: it means that even when access to the
global Internet is blocked, it should still be possible to communicate
with other devices on local networks or national subsets of the Internet.
While other mechanisms could still influence the ability to form mesh
networks, the Android operating system itself doesn't seem to get in our
way.

## Thanks

This experiment was part of ongoing research funded by
[eQualitie](https://equalit.ie/).

## About Briar

Briar is a messaging app designed for activists, journalists,
and anyone else who needs a safe, easy and robust way to communicate.
Unlike traditional messaging tools such as email, Twitter or Telegram,
Briar doesn't rely on a central server -
messages are synchronized directly between the users' devices.
If the internet's down,
Briar can sync via Bluetooth or Wi-Fi, keeping the information flowing in a crisis.
If the internet's up, Briar can sync via the Tor network, protecting users
and their relationships from surveillance.

{{% funding %}}

{{< contact  >}}

Twitter: [@BriarApp](https://twitter.com/BriarApp)

Mastodon: [@Briar](https://fosstodon.org/@briar)
