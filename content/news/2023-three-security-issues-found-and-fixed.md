---
aliases:
- /news/2023-three-security-issues-found-and-fixed.html
date: 2023-05-24T11:00:00+00:00
title: "Three security issues found and fixed"
---

In February of this year, security researchers at
[ETH Zürich](https://appliedcrypto.ethz.ch/) notified us that they had found
three security issues in the Briar app. Two of these issues were fixed in
version 1.4.22 of Briar, which was released in February. The third issue was
fixed in version 1.5.3, which is being released today. All users are
encouraged to upgrade to version 1.5.3 of the app as soon as possible.

We have not received any reports of these bugs being exploited in the wild,
and the third issue is not exploitable.

We would like to apologise for the design and implementation mistakes that led
to these issues, and to thank Yuanming Song and Prof. Kenny Paterson for
finding the issues and responsibly disclosing them to us.

We have requested an independent security audit of Briar's protocol stack to
ensure that no other issues remain undiscovered.

For those who are interested in the details, a description of each issue is
given below. The researchers' report can be found [here](https://ethz.ch/content/dam/ethz/special-interest/infk/inst-infsec/appliedcrypto/education/theses/report_YuanmingSong.pdf).

## Issue 1: Receiving invalid message would have caused app to exit

The first issue (fixed in Briar 1.4.22) would have allowed a malicious user to
prevent their contacts from using Briar by repeatedly sending them invalid
messages that would cause the app to exit.

Receiving a message longer than the maximum allowed length should have raised
an error that would cause the invalid message to be discarded. Instead, the
check raised a different type of error that would cause the app to exit.

There was no risk of memory corruption, as the length check took place in
memory-safe Java code. Invalid messages were not stored or forwarded to other
users.

## Issue 2: Message duplication in blogs, forums and private groups

The second issue (fixed in Briar 1.4.22) would have allowed a malicious user
to create duplicates of messages written by other users in blogs, forums and
private groups. The duplicates would have had the same content and timestamps
as the originals, but would have appeared alongside the originals as though
they were separate messages from the same authors.

To explain this issue we need to give some background information about the
structure of Briar messages.

Every message in Briar consists of a timestamp, a group identifier and a
message body. Each message has a unique identifier that is calculated by
hashing these fields.

Different features of the app use these fields in different ways. The blog,
forum and private group features make use of digital signatures: the body of
each message contains some content along with a digital signature by the
author of the content. The signature covers the content as well as the
timestamp, the group identifier and the author's Briar identity.

When verifying the signature on a message, Briar deserialises the message body
to extract the content and signature, then serialises the content, timestamp,
group identifier and author's Briar identity to recreate the exact information
that was originally signed. This ensures that none of these fields can be
altered without invalidating the signature.

The ETH Zürich researchers discovered that this process of deserialising the
message body and then reserialising the content to verify the signature made
it possible to take a message signed by another user and produce a message
with a different body (and therefore a different unique identifier) that would
nevertheless be identical to the original after deserialisation and
reserialisation. Thus the signature from the original message would still be
valid, and there would appear to be two identical messages signed by the same
author.

It would not have been possible to alter the content, timestamp, group
identifier or Briar identity without invalidating the signature, but the
duplicate messages might have caused confusion.

This issue occurred because Briar did not check that the message body was
serialised in canonical form before deserialising it, so it was possible to
create multiple non-canonical representations of the same message body, which
would all be converted into the same canonical form after deserialisation and
reserialisation.

Fortunately, genuine messages in blogs, forums and private groups have always
been created in canonical form, so the issue was solved by rejecting any
messages that were not in canonical form.

## Issue 3: Poorly designed cryptographic handshake

The third issue (fixed in Briar 1.5.3) involved a poorly designed
cryptographic handshake. At first it appeared that design flaws in this
handshake could have allowed network traffic between Briar users to be
decrypted by an attacker who had successfully carried out a specific set of
other attacks against those users. Fortunately, we were able to confirm that
this was not possible thanks to an extra layer of cryptographic protection
provided by the Tor network. The issue was not exploitable and there was no
danger to users. Even so, Briar 1.5.3 replaces the insecure handshake with a
more secure version.

The handshake in question is part of the Bramble Handshake Protocol (BHP),
which is used when users add each other as contacts by exchanging Briar links.
The purpose of BHP is to derive a shared secret that is known to both users
but not to anyone else, include anyone who may be eavesdropping on the network
connection used for the handshake. The shared secret is ephemeral, meaning
that it should not be possible to recreate the shared secret using any
information that is retained by the users after the handshake.

BHP did not meet these design criteria. An adversary who was able to eavesdrop
on the connection that was used for the handshake, and was later able to
compromise both users' Briar accounts, could have decrypted network traffic
between the users that was sent between the time of the handshake and the time
of the account compromises.

Fortunately, we were able to confirm that the eavesdropping part of the attack
was not achievable. The connections used for BHP handshakes are always made
via the Tor network, using version 3 of Tor's hidden service protocol. Through
discussions with the developers of Tor we were able to confirm that this
protocol uses strong encryption that would have prevented an adversary from
eavesdropping on BHP handshakes. Without being able to eavesdrop, an adversary
could not later decrypt past network traffic even if both users' accounts were
compromised.

The poor design of the BHP handshake was a serious mistake on our part.
Fortunately, thanks to the extra layer of protection provided by Tor, users
were not put at risk by this mistake.

Briar 1.5.3 replaces the insecure handshake with a more secure version, and we
have requested an independent security audit of the whole protocol stack to
ensure that no other mistakes of this kind were made.

## About Briar

Briar is a messaging app designed for activists, journalists, and anyone else
who needs a safe, easy and robust way to communicate. Unlike traditional
messaging tools such as email, Twitter or Telegram, Briar doesn't rely on a
central server - messages are synchronized directly between the users'
devices. If the internet's down, Briar can sync via Bluetooth or Wi-Fi,
keeping the information flowing in a crisis. If the internet's up, Briar can
sync via the Tor network, protecting users and their relationships from
surveillance.

{{% funding %}}

{{< contact  >}}

Twitter: [@BriarApp](https://twitter.com/BriarApp)

Mastodon: [@Briar](https://fosstodon.org/@briar)
