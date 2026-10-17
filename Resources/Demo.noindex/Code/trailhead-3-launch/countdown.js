// Trailhead 3's launch page has two phases. Until Tuesday, November 3, 2026, at 9:00 CET it counts down and takes
// emails for the launch-day notice; from then on it sells. At zero, html[data-phase] goes from "soon" to "live" and
// styles.css does the rest. No reload: nobody who is waiting on the page hits the server at 9:00:00 sharp.
//
// It counts with the server's clock, not the visitor's: a laptop running five minutes fast would show the buy button
// before the shop turns the product on. To try any moment, add ?now= to the address, for example
// ?now=2026-11-03T08:59:50%2B01:00 to watch it reach zero (%2B is the + of the time zone).

const LAUNCH = Date.parse("2026-11-03T09:00:00+01:00"); // CET, not CEST: the clocks go back on October 25

let offset = 0; // the server's time minus this device's, in milliseconds
const now = () => Date.now() + offset;

// ?now=: the page behaves as if it were that moment, and its clock runs on from there.
function testOffset() {
  const value = new URLSearchParams(location.search).get("now");
  const at = value ? Date.parse(value) : NaN;
  return Number.isNaN(at) ? null : at - Date.now();
}

// The Date header of a HEAD request for this page. It's to the second, which is all a countdown needs; the 500 ms
// put the truncated second back in the middle.
async function serverOffset() {
  try {
    const sent = Date.now();
    const response = await fetch(location.href, {
      method: "HEAD",
      cache: "no-store",
      signal: AbortSignal.timeout(2000),
    });
    const date = Date.parse(response.headers.get("Date") ?? "");
    return Number.isNaN(date) ? 0 : date + 500 - (sent + Date.now()) / 2;
  } catch {
    return 0;
  }
}

// Rounded up, so the last second reads 00:00:01 and the page turns live as it reaches zero.
function parts(ms) {
  const seconds = Math.ceil(ms / 1000);
  return {
    days: Math.floor(seconds / 86_400),
    hours: Math.floor(seconds / 3_600) % 24,
    minutes: Math.floor(seconds / 60) % 60,
    seconds: seconds % 60,
  };
}

const digits = Object.fromEntries(
  [...document.querySelectorAll("[data-unit]")].map((element) => [element.dataset.unit, element]),
);
const sentence = document.querySelector("[data-countdown-sentence]");
const plural = (count, one, many) => `${count} ${count === 1 ? one : many}`;

function show(left) {
  const time = parts(left);
  for (const [unit, value] of Object.entries(time)) digits[unit].textContent = String(value).padStart(2, "0");
  sentence.textContent =
    `Faltan ${plural(time.days, "día", "días")}, ${plural(time.hours, "hora", "horas")} y ` +
    `${plural(time.minutes, "minuto", "minutos")} para el lanzamiento.`;
}

// Recomputed from the clock every time, so a tab the browser throttled, or a laptop that slept, is right again on its
// next tick.
function tick() {
  const left = LAUNCH - now();
  if (left <= 0) {
    document.documentElement.dataset.phase = "live";
    return;
  }
  show(left);
  setTimeout(tick, left % 1000 || 1000);
}

// The launch-day notice. Without JavaScript the form still posts, and the server answers with a page that says the
// same as these messages.
const form = document.querySelector(".notify");
const status = document.querySelector("[data-notify-status]");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = form.querySelector("button");
  button.disabled = true;
  try {
    const response = await fetch(form.action, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: String(new FormData(form).get("email")).trim() }),
    });
    if (!response.ok) throw new Error(`notify: ${response.status}`);
    form.reset();
    status.textContent = "Hecho. Te escribiremos el 3 de noviembre a las 9:00, y solo ese día.";
  } catch {
    status.textContent = "No hemos podido apuntarte. Prueba otra vez en un momento.";
  } finally {
    button.disabled = false;
  }
});

offset = testOffset() ?? (await serverOffset());
tick();
