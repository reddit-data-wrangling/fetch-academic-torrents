# Movies panel selection

Status: 42-community pilot approved for acquisition on 2026-08-04.

The pilot contains only communities verified in the 2026-07-30 Arctic Shift
catalogue snapshot. Its expected archive volume is approximately 136.0 million
records. It samples the film ecosystem across seven strata without treating
the 169-candidate catalogue as a fetch queue.

## Panel design

- General discussion includes mainstream, critical, recommendation, review,
  and social-logging populations.
- Industry, exhibition, awards, production, and filmmaking crafts are sampled
  separately from film audiences.
- The genre stratum spans large and small populations and includes
  documentary, cult, found-footage, and experimental forms.
- International cinema includes broad discovery plus communities centred on
  Japan, Korea, India, Africa, and Ireland. English-language Reddit coverage is
  not presented as a complete global frame.
- Physical media and preservation are separated from studios/labels.

## Exclusions and expansion gate

Missing and restricted communities are ineligible. Broad communities where
film is incidental (`memes`, `creepy`, generic entertainment, hardware, and
general streaming services) are not in the pilot. Anime, broad animation,
fantasy, and science-fiction communities are deferred because their medium
boundaries need cross-collection review. Title-, sequel-, and franchise-level
communities remain out of scope. Director communities are deliberately
deferred until the pilot passes volume and content-quality checks.

Acquisition runs globally smallest-first alongside the comics pilot and loads
both submissions and comments into MongoDB `reddit` at
`mongodb://localhost:27019`. Shared raw files and MongoDB ID upserts make
intentional cross-collection overlap safe.
