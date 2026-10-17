# Trailhead 3 · launch page

The page at **contoso.com/trailhead-3**. Owner: Sara Navarro. Copy and brief: Lucía Romero and Marta Gil.

Three files and no build step: `index.html`, `styles.css` and `countdown.js`. The page has two phases, set by
`data-phase` on `<html>`:

| Phase | When | Shows |
| --- | --- | --- |
| `soon` | until Tue, November 3, 2026, 9:00 CET | the date, the countdown, the teaser and the **Avísame** form |
| `live` | from then on | **Comprar · 249 €**, *Pruébala en una tienda* and the setup guide video |

## Dates

| Date | What happens |
| --- | --- |
| Tue, Oct 27 | The page goes public with the teaser video, the countdown and the notify form. |
| Wed, Oct 28 | The product photos arrive and replace the spec sheet's drawing in the hero. |
| Mon, Nov 2 | Last day for changes. After that, only Sara deploys, and only fixes. |
| Tue, Nov 3, 9:00 | The page switches to **Comprar**, the shop turns the product on, and everyone on the notify list gets one email, with the newsletter. |
| Wed, Nov 4 | The notify list is deleted, as the form promises. |

## What the page can and can't say

From Lucía's brief (her voice memo of October 7) and Legal:

- Lead with the weight: **1,9 kg, 300 g less than Trailhead 2**.
- Say the fly is made from recycled polyester.
- "Nuestra tienda más ligera" is fine. **"La más ligera del mercado" is not**: we can't prove it.
- The three numbers are the same as the stores' poster: **1,9 kg · 3 personas · 3 minutos**.

Every figure comes from the spec sheet. If the page and the spec sheet ever disagree, the spec sheet wins: fix the
page.

## The countdown

- It counts to **9:00 CET** (UTC+01:00). The clocks go back on October 25, so it isn't CEST.
- It uses the server's clock, from the `Date` header of a `HEAD` request for the page, so a device whose clock is
  wrong doesn't show the buy button early. If the request fails, it uses the device's clock.
- At zero it sets `data-phase="live"` without reloading, so nobody waiting on the page hits the server at 9:00:00.
- At 9:00 the release also republishes `index.html` with `data-phase="live"`, for visitors without JavaScript and
  for search engines.
- The countdown digits are hidden from screen readers. They read one sentence instead: "Faltan 18 días, 3 horas y
  12 minutos para el lanzamiento."

## Try it locally

```sh
python3 -m http.server 8080
```

Then open <http://localhost:8080/?now=2026-11-03T08:59:50%2B01:00> to watch it reach zero, or any other moment with
`?now=` (`%2B` is the `+` of the time zone). Locally the notify form shows its error message, because
`/api/trailhead-3/notify` lives in the shop's API.

## Videos

`media/` isn't in git. Copy the two videos from the campaign folder:

| Copy | As |
| --- | --- |
| `Video/Trailhead 3 – teaser.mp4` | `media/trailhead-3-teaser.mp4` |
| `Video/Trailhead 3 – setup guide.mp4` | `media/trailhead-3-setup-guide.mp4` |

The social cuts of the teaser (9:16 and 1:1) are made with `scripts/social_cuts.sh`.

---

Contoso Outdoor is a fictitious company. This page is sample content.
