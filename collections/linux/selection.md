# Linux panel selection

Status: N=99 panel authorised on 2026-07-31; 93 require acquisition.

Known existing MongoDB holdings for this collection include `linux`,
`linuxquestions`, `linux4noobs`, `osdev`, `kernel`, and `linusrants` according to the
[operations log](../../docs/operations/collection-log.md).
MongoDB `reddit` on port 27017 was audited before selection. `linux`,
`linuxquestions`, `linux4noobs`, `osdev`, and `kernel` are already present in
both MongoDB collections, so they are retained as known holdings but excluded
from this acquisition queue. `linusrants` is also retained as a collected Linux
panel member.

The next selection should be stratified across:

- kernel and low-level development;
- distribution-neutral discussion and support;
- distributions;
- desktop environments, display systems, and window managers;
- administration, containers, virtualization, and self-hosting;
- embedded, mobile, gaming, and specialist Linux systems;
- platform stacks such as packaging, filesystems, graphics, and audio.

The authorised Linux panel is a broad census of all 99 candidates verified by
Arctic Shift. `linusrants` is classified as a Linux member and was already
available alongside five other panel communities in both MongoDB collections
at selection time, leaving 93 acquisition targets. Missing and restricted
candidates are excluded. Acquisition targets run smallest-first; each capture
is validated and loaded into MongoDB before the next target.
