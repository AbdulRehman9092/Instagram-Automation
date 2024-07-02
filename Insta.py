import time
import random
import json
from seleniumbase import SB

USERNAME = "Your Username"
PASSWORD = "Your Pass"
INSTAGRAM_URLS_FOR_LOGIN = {
    "https://www.instagram.com",
    "https://www.instagram.com/",
}

def login(sb: SB):
    sb.type('input[name="username"]', USERNAME)
    sb.type('input[name="password"]', PASSWORD)
    sb.click("form#loginForm div:nth-of-type(3) button")

#U can scrape followers of an id by growman extension. and put their usernames here.
def follow(sb):
    username_list = """
        simba07.22
        carlosmxs
        wilberbenito
        ali.gohari4

        """
    USERNAMES = [u.strip() for u in username_list.splitlines() if u.strip()]

    # persistent dead follow list file so next runs will skip those usernames
    dead_file = "dead_follow.txt"
    try:
        with open(dead_file, "r", encoding="utf-8") as f:
            dead = {line.strip() for line in f if line.strip()}
    except Exception:
        dead = set()
    n = random.randint(1, 2)

    # select first n usernames that are NOT in dead list (left-to-right)
    selected = []
    for u in USERNAMES:
        if u in dead:
            continue
        selected.append(u)
        if len(selected) == n:
            break

    if not selected:
        print("No available usernames to follow (all usernames are in dead_follow.txt).")
        return False

    # Process each selected username one-by-one
    for idx, target_user in enumerate(selected, start=1):
        profile_url = f"https://www.instagram.com/{target_user}/"
        print(f"Processing (follow): {target_user} -> {profile_url}")

        try:
            # Try to open profile and perform the follow click
            sb.open(profile_url)
            time.sleep(random.uniform(1.5, 3.0))

            # Attempt to click the Follow button (may raise if not present)
            try:
                sb.click('button:contains("Follow")', timeout=5)
                print(f"Clicked Follow for {target_user} (if button present).")
            except Exception as e:
                # log but don't stop — we will still add to dead list below
                print(f"Follow-click failed for {target_user}: {e}")

        except Exception as e:
            # any open/profile navigation error is logged but does not stop the loop
            print(f"Failed to open or process profile for {target_user}: {e}")

        finally:
            # ALWAYS add the username to the dead follow set no matter what happened
            dead.add(target_user)
            print(f"Added to dead follow list: {target_user}")

            # sleep between users to reduce rate-limiting risk
            sleep_time = random.uniform(3, 7)
            print(f"Sleeping for {sleep_time:.1f}s before next user... ({idx}/{len(selected)})")
            time.sleep(sleep_time)

    # write updated dead follow list back to disk
    try:
        with open(dead_file, "w", encoding="utf-8") as f:
            for d in sorted(dead):
                f.write(d + "\n")
    except Exception as e:
        print("Failed to update dead_follow.txt:", e)

    # finished run
    return True


def message(sb):
    #input all messages u want to send randomly
    MESSAGE_TEXT = ["Recognize me?", "Remember me?", "Who is this at this hour?", "Miss me yet?", "Guess who is texting", "Did you just think of me?", "Are you awake or dreaming", "I have a tiny secret", "Phone on silent or fake", "Call me if you dare", "Coffee or wine tonight", "Are you trouble or fun", "Did you say my name today", "Tell me one truth now", "Want to play a little game", "I may be closer than you think", "Say hi and make my day", "Admit it you smiled", "If I show up will you run", "I am bored entertain me", "Text back and earn a surprise", "Think fast who am I", "I lost a bet now answer", "Want to ruin your plans", "You plus me equals what", "Be honest do you miss me", "Can you keep a secret", "I have a question for you", "Guess where I am right now", "Did you plan to make me smile", "Message me two words only", "Dare me to visit tonight", "I am not who you expect", "Tell me your guilty pleasure", "Stop scrolling and say hello", "Your voice or my laugh which wins", "Are you hiding from me", "Say my name and prove it", "Ready for a small adventure", "Last chance to say hi"]

    username_list = """
        ad.a690
        a.jower
        ali_rhm_31

        """
    USERNAMES = [u.strip() for u in username_list.splitlines() if u.strip()]
    dead_file = "dead_usernames.txt"
    try:
        with open(dead_file, "r", encoding="utf-8") as f:
            dead = {line.strip() for line in f if line.strip()}
    except Exception:
        dead = set()
    n = random.randint(1, 1)

    # select first n usernames that are NOT in dead list (left-to-right)
    selected = []
    for u in USERNAMES:
        if u in dead:
            continue
        selected.append(u)
        if len(selected) == n:
            break

    if not selected:
        print("No available usernames to message (all usernames are in dead list).")
        return False

    # choose messages: sample without replacement when possible, otherwise allow repeats
    if len(MESSAGE_TEXT) >= len(selected):
        msgs = random.sample(MESSAGE_TEXT, len(selected))
    else:
        msgs = [random.choice(MESSAGE_TEXT) for _ in selected]

    # send messages to selected users (preserving your original single-user send logic)
    for idx, (target_user, msg_text) in enumerate(zip(selected, msgs), start=1):
        profile_url = f"https://www.instagram.com/{target_user}/"
        print(f"Processing: {target_user} -> {profile_url}")

        try:
            # Try to open profile and run your original flows.
            sb.open(profile_url)
            time.sleep(random.uniform(1.5, 3.0))

            # First message-box attempt (kept as you had it)
            try:
                buttons = sb.find_elements("div[role='button']")
                for btn in buttons:
                    if btn.text and btn.text.strip() == "Message":
                        btn.click()
                        break
                else:
                    raise Exception("No exact 'Message' button found")
                # use the chosen msg_text here
                sb.type('div[aria-label="Message"]', msg_text)
                sb.click('div[aria-label="Send"]')
            except Exception as e:
                print(f"Note: initial message box flow failed for {target_user}: {e}")

            # Options -> Send message flow (kept as you had it)
            try:
                sb.click('svg[aria-label="Options"]')
                sb.click('button:contains("Send message")', timeout=5)
                if sb.is_element_visible('button:contains("Not Now")'):
                    sb.click('button:contains("Not Now")')
                sb.type('div[aria-label="Message"] p', msg_text)
                if sb.is_element_visible('button:contains("Not Now")'):
                    sb.click('button:contains("Not Now")')
                sb.click('div[role="button"]:contains("Send")')
                print(f"Attempted send UI for {target_user}.")
            except Exception as e:
                print(f"Failed to complete send UI for {target_user}: {e}")

        except Exception as e:
            # Any error opening profile or unexpected error — we log it but continue.
            print(f"Failed to open or process profile for {target_user}: {e}")

        finally:
            # --- CRITICAL: add username to dead set no matter what happened ---
            dead.add(target_user)
            print(f"Added to dead list (regardless of outcome): {target_user}")

            # sleep between users to reduce rate-limiting risk
            sleep_time = random.uniform(3, 7)
            print(f"Sleeping for {sleep_time:.1f}s before next user... ({idx}/{len(selected)})")
            time.sleep(sleep_time)

    # write updated dead list back to disk
    try:
        with open(dead_file, "w", encoding="utf-8") as f:
            for d in sorted(dead):
                f.write(d + "\n")
    except Exception as e:
        print("Failed to update dead list file:", e)

    # finished batch run
    return True


def explore(sb):
    url = "https://www.instagram.com/explore/"
    n = random.choice([2, 3])
    for _ in range(n):
        sb.open(url)
        sb.wait_for_ready_state_complete()
        sb.execute_script("""
(async function (){
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const randInt = (min, max) => Math.floor(Math.random()*(max-min+1)) + min;
  const sleepRange = (minMs, maxMs) => sleep(randInt(minMs, maxMs));
  // probabilities you requested:
  const likeProbability = 0.09;    // 0% chance to like
  const commentProbability = 0.2; // 70% chance to comment
  const randChance = p => Math.random() < p;

  // --- helpers (kept from prior working version) ---
  function isVisible(el){
    if(!el) return false;
    const s = getComputedStyle(el);
    if(s.display === 'none' || s.visibility === 'hidden' || Number(s.opacity) === 0) return false;
    const r = el.getBoundingClientRect();
    return r.width > 1 && r.height > 1 && r.bottom > 0 && r.top < window.innerHeight;
  }

  function getClickableAncestor(el){
    if(!el) return null;
    let cur = el;
    for(let i=0;i<12 && cur;i++){
      const tag = cur.tagName;
      const role = cur.getAttribute && cur.getAttribute('role');
      const ti = cur.getAttribute && cur.getAttribute('tabindex');
      const cs = getComputedStyle(cur);
      if(tag === 'BUTTON' || tag === 'A' || role === 'button' || ti !== null || cs.cursor === 'pointer' || typeof cur.onclick === 'function') return cur;
      cur = cur.parentElement;
    }
    return el;
  }

  function clickEl(el){
    if(!el) return false;
    try{ el.scrollIntoView({block:'center', inline:'center', behavior:'auto'}); }catch(e){}
    const ev = new MouseEvent('click', { bubbles: true, cancelable: true, view: window });
    el.dispatchEvent(ev);
    return true;
  }

  // robustClickLike (unchanged, robust pointer + click sequences)
  async function robustClickLike(svg){
    if(!svg){ console.warn('robustClickLike: no svg'); return false; }
    try{ svg.scrollIntoView({block:'center', inline:'center', behavior:'auto'}); }catch(e){}
    await sleep(200);

    const rect = svg.getBoundingClientRect();
    const cx = Math.round(rect.left + rect.width/2);
    const cy = Math.round(rect.top + rect.height/2);

    async function tryOnTarget(target, label){
      if(!target) return false;
      try{ target.scrollIntoView({block:'center', inline:'center', behavior:'auto'}); }catch(e){}
      await sleep(60);

      try {
        if(typeof target.click === 'function'){
          target.click();
          console.log('tryOnTarget: native click() succeeded on', label, target);
          return true;
        }
      } catch(e){
        console.warn('tryOnTarget: native click() threw', label, e);
      }

      const pointerTypes = ['mouse','touch'];
      for(const pType of pointerTypes){
        const opts = { bubbles:true, cancelable:true, clientX:cx, clientY:cy, pointerId:1, pointerType:pType, isPrimary:true };
        try{
          target.dispatchEvent(new PointerEvent('pointerover', opts));
          target.dispatchEvent(new PointerEvent('pointerenter', opts));
          target.dispatchEvent(new MouseEvent('mouseover', opts));
          target.dispatchEvent(new MouseEvent('mouseenter', opts));
          target.dispatchEvent(new PointerEvent('pointerdown', opts));
          target.dispatchEvent(new MouseEvent('mousedown', opts));
          await sleep(8);
          target.dispatchEvent(new PointerEvent('pointerup', opts));
          target.dispatchEvent(new MouseEvent('mouseup', opts));
          target.dispatchEvent(new MouseEvent('click', Object.assign({}, opts)));
          console.log(`tryOnTarget: pointer(${pType}) sequence dispatched on`, label, target);
          return true;
        }catch(err){
          console.warn(`tryOnTarget: pointer(${pType}) failed on ${label}`, err);
        }
      }

      try{
        const ev = new MouseEvent('click', { bubbles:true, cancelable:true, clientX:cx, clientY:cy });
        target.dispatchEvent(ev);
        console.log('tryOnTarget: dispatched raw MouseEvent click on', label, target);
        return true;
      }catch(e){ /* ignore */ }

      return false;
    }

    const closestClickable = svg.closest('button, a, [role="button"], [tabindex]');
    if(closestClickable && closestClickable !== svg){
      console.log('robustClickLike: trying closest clickable ancestor:', closestClickable);
      if(await tryOnTarget(closestClickable, 'closestClickable')) return true;
    }

    const elAtCenter = document.elementFromPoint(cx, cy);
    if(elAtCenter && elAtCenter !== svg){
      console.log('robustClickLike: trying elementFromPoint at center:', elAtCenter);
      const elAtCenterClickable = elAtCenter.closest('button, a, [role="button"], [tabindex]') || getClickableAncestor(elAtCenter);
      if(elAtCenterClickable && elAtCenterClickable !== closestClickable){
        if(await tryOnTarget(elAtCenterClickable, 'elementFromPoint.clickableAncestor')) return true;
      }
      if(await tryOnTarget(elAtCenter, 'elementFromPoint')) return true;
    }

    console.log('robustClickLike: trying svg itself');
    if(await tryOnTarget(svg, 'svg')) return true;

    const cover = document.elementFromPoint(cx, cy);
    if(cover && cover !== svg){
      const old = cover.style.pointerEvents;
      console.warn('robustClickLike: disabling pointer-events on covering element', cover);
      cover.style.pointerEvents = 'none';
      await sleep(80);
      try{
        const cand = closestClickable || svg;
        if(await tryOnTarget(cand, 'after-disable-overlay')) {
          cover.style.pointerEvents = old;
          return true;
        }
      }catch(e){
        console.warn('robustClickLike: error after disabling overlay', e);
      } finally {
        cover.style.pointerEvents = old;
      }
    }

    for(let i=0;i<3;i++){
      await sleep(150 + i*80);
      const fresh = document.elementFromPoint(cx, cy) || svg;
      const cand = fresh.closest('button, a, [role="button"], [tabindex]') || fresh;
      console.log('robustClickLike: retrying candidate', i, cand);
      if(await tryOnTarget(cand, 'final-retry-'+i)) return true;
    }

    console.error('robustClickLike: all attempts failed. Diagnostics:', {
      svgOuterHTML: (svg.outerHTML || '').slice(0,400),
      svgRect: svg.getBoundingClientRect ? svg.getBoundingClientRect() : null,
      elementAtCenter: document.elementFromPoint(cx, cy),
      closestClickable: closestClickable && (closestClickable.outerHTML || closestClickable)
    });
    return false;
  }

  // --- find comment input inside the post container for a given element (svg) ---
  function findCommentInputInsidePost(anchorEl){
    if(!anchorEl) return null;
    let cur = anchorEl;
    for(let depth=0; depth<12 && cur; depth++){
      const selectors = [
        'textarea[aria-label^="Add a comment"]',
        'textarea[placeholder^="Add a comment"]',
        'textarea[aria-label*="Add a comment"]',
        'textarea[placeholder*="Add a comment"]',
        'div[contenteditable="true"][aria-label*="Add a comment"]',
        'div[role="textbox"][contenteditable="true"]',
        'div[contenteditable="true"]'
      ];
      for(const sel of selectors){
        const ta = cur.querySelector(sel);
        if(ta && isVisible(ta)) return ta;
      }
      const anyTa = Array.from(cur.querySelectorAll('textarea')).find(t=>isVisible(t));
      if(anyTa) return anyTa;
      cur = cur.parentElement;
    }
    const globalCandidates = Array.from(document.querySelectorAll('textarea[aria-label*="Add a comment"], textarea[placeholder*="Add a comment"], textarea')).filter(isVisible);
    return globalCandidates.length ? globalCandidates[0] : null;
  }

  // --- find Post button inside the same post container; avoid share button ---
  function findPostButtonInContainer(anchorEl){
    if(!anchorEl) return null;
    let cur = anchorEl;
    for(let depth=0; depth<12 && cur; depth++){
      const candidates = Array.from(cur.querySelectorAll('[role="button"], button, div[tabindex]'));
      for(const c of candidates){
        if(!isVisible(c)) continue;
        if(c.querySelector && c.querySelector('svg[aria-label="Share Post"], svg[title="Share Post"]')) continue;
        const txt = (c.innerText || c.textContent || '').trim().toLowerCase();
        if(txt === 'post' || /^post\b/i.test(txt)) return c;
      }
      cur = cur.parentElement;
    }
    const globalCandidates = Array.from(document.querySelectorAll('[role="button"], button, div[tabindex]')).filter(c => isVisible(c) && !(c.querySelector && c.querySelector('svg[aria-label="Share Post"], svg[title="Share Post"]')));
    for(const c of globalCandidates){
      const txt = (c.innerText || c.textContent || '').trim().toLowerCase();
      if(txt === 'post' || /^post\b/i.test(txt)) return c;
    }
    return null;
  }

  // --- typed input routine (keeps robust multi-strategy approach) ---
  async function fillCommentInput(inputEl, text){
    if(!inputEl) return false;
    function setNativeValue(el, value){
      const proto = Object.getPrototypeOf(el);
      const desc = Object.getOwnPropertyDescriptor(proto, 'value');
      if(desc && desc.set) desc.set.call(el, value);
      else el.value = value;
    }

    try{
      inputEl.focus && inputEl.focus();
      try{ inputEl.dispatchEvent(new CompositionEvent('compositionstart', {bubbles:true, cancelable:false, data:''})); }catch(e){}
      setNativeValue(inputEl, text);
      try{
        inputEl.dispatchEvent(new InputEvent('input', {bubbles:true, cancelable:true, data:text, inputType:'insertFromPaste'}));
      }catch(e){
        const ev = document.createEvent('Event'); ev.initEvent('input', true, true); inputEl.dispatchEvent(ev);
      }
      try{ inputEl.dispatchEvent(new CompositionEvent('compositionend', {bubbles:true, cancelable:false, data:text})); }catch(e){}
      inputEl.dispatchEvent(new Event('change', {bubbles:true}));
      await sleep(120);
      if((inputEl.value && inputEl.value.trim() === text.trim()) || (inputEl.isContentEditable && (inputEl.innerText||'').trim() === text.trim())) return true;
    }catch(e){ console.warn('fillCommentInput: paste-like attempt failed', e); }

    if(inputEl.isContentEditable || (inputEl.getAttribute && inputEl.getAttribute('contenteditable') === 'true')){
      try{
        inputEl.focus && inputEl.focus();
        try{ document.execCommand('selectAll'); document.execCommand('delete'); }catch(e){}
        try{
          if(document.queryCommandSupported && document.queryCommandSupported('insertText')){
            document.execCommand('insertText', false, text);
          } else {
            inputEl.innerText = text;
          }
        }catch(e){ inputEl.innerText = text; }
        inputEl.dispatchEvent(new InputEvent('input', {bubbles:true, cancelable:true, data:text, inputType:'insertFromPaste'}));
        inputEl.dispatchEvent(new Event('change', {bubbles:true}));
        await sleep(120);
        if((inputEl.innerText||'').trim() === text.trim()) return true;
      }catch(err){ console.warn('fillCommentInput: execCommand attempt failed', err); }
    }

    try{
      inputEl.focus && inputEl.focus();
      setNativeValue(inputEl, '');
      inputEl.dispatchEvent(new InputEvent('input', {bubbles:true, cancelable:true, data:'', inputType:'deleteContentBackward'}));
      for(let i=0;i<text.length;i++){
        const ch = text[i];
        const kd = new KeyboardEvent('keydown', {key: ch, char: ch, bubbles:true, cancelable:true});
        const kp = new KeyboardEvent('keypress', {key: ch, char: ch, bubbles:true, cancelable:true});
        inputEl.dispatchEvent(kd);
        inputEl.dispatchEvent(kp);
        const current = (inputEl.value || '') + ch;
        setNativeValue(inputEl, current);
        inputEl.dispatchEvent(new InputEvent('input', {bubbles:true, cancelable:true, data:ch, inputType:'insertText'}));
        inputEl.dispatchEvent(new KeyboardEvent('keyup', {key: ch, char: ch, bubbles:true}));
        await sleep(70 + Math.floor(Math.random()*30));
      }
      inputEl.dispatchEvent(new Event('change', {bubbles:true}));
      await sleep(120);
      if((inputEl.value && inputEl.value.trim() === text.trim()) || (inputEl.isContentEditable && (inputEl.innerText||'').trim() === text.trim())) return true;
    }catch(e){ console.warn('fillCommentInput: per-char typing fallback failed', e); }

    try{
      setNativeValue(inputEl, text);
      inputEl.dispatchEvent(new Event('input', {bubbles:true}));
      inputEl.dispatchEvent(new Event('change', {bubbles:true}));
      await sleep(120);
      return true;
    }catch(e){ console.warn('fillCommentInput: final fallback failed', e); }

    return false;
  }

  // wait until a Post button becomes clickable inside the container (up to timeout)
  async function waitUntilPostClickable(anchorEl, timeout = 3000){
    const start = Date.now();
    while(Date.now() - start < timeout){
      const btn = findPostButtonInContainer(anchorEl);
      if(btn && isVisible(btn)){
        const cs = getComputedStyle(btn);
        const pe = cs.pointerEvents;
        const disabled = btn.getAttribute && (btn.getAttribute('disabled') !== null || btn.getAttribute('aria-disabled') === 'true');
        if(pe !== 'none' && !disabled){
          if(!(btn.querySelector && btn.querySelector('svg[aria-label="Share Post"], svg[title="Share Post"]'))){
            return btn;
          }
        }
      }
      await sleep(120);
    }
    return null;
  }

  // findPostButtonInContainer (kept)
  function findPostButtonInContainer(anchorEl){
    if(!anchorEl) return null;
    let cur = anchorEl;
    for(let depth=0; depth<12 && cur; depth++){
      const candidates = Array.from(cur.querySelectorAll('[role="button"], button, div[tabindex]'));
      for(const c of candidates){
        if(!isVisible(c)) continue;
        if(c.querySelector && c.querySelector('svg[aria-label="Share Post"], svg[title="Share Post"]')) continue;
        const txt = (c.innerText || c.textContent || '').trim().toLowerCase();
        if(txt === 'post' || /^post\b/i.test(txt)) return c;
      }
      cur = cur.parentElement;
    }
    const globalCandidates = Array.from(document.querySelectorAll('[role="button"], button, div[tabindex]')).filter(c => isVisible(c) && !(c.querySelector && c.querySelector('svg[aria-label="Share Post"], svg[title="Share Post"]')));
    for(const c of globalCandidates){
      const txt = (c.innerText || c.textContent || '').trim().toLowerCase();
      if(txt === 'post' || /^post\b/i.test(txt)) return c;
    }
    return null;
  }

  // waitForVisibleLike (WeakSet)
  async function waitForVisibleLike(seenWeakSet, timeout = 3500, poll = 150){
    const start = Date.now();
    while(Date.now() - start < timeout){
      let svgs = Array.from(document.querySelectorAll('div.x6s0dn4 svg[aria-label="Like"], svg[aria-label="Like"]'));
      svgs = svgs.filter(isVisible);
      const fresh = [];
      for(const sv of svgs) if(!seenWeakSet.has(sv)) fresh.push(sv);
      if(fresh.length) return fresh;
      await sleep(poll);
    }
    return [];
  }

  // ---------------------------
  // Main randomized single-slide loop (open carousel once)
  // ---------------------------
  const comments = ["Oh really", "Who told you that you can look like this", "Stop stealing my oxygen with this post", "Confess who styled this crime scene", "Emergency hotline for this level of cute", "Okay but explain the energy source", "Save some chaos for the rest of us", "Where do I enroll for your vibe class", "Plot twist please I need context", "Why does this make my phone heat up", "Hold up this is suspiciously flawless", "You are being illegally attractive", "Tell me the secret ingredient", "This is peak mood I need receipts", "Stop normal acting like that", "Someone call the fashion police now", "Are you sponsored by charisma", "I demand a behind the scenes", "Who is behind this glow up machine", "Okay I am officially intrigued", "Teach me one hack or two", "This post is fueling my FOMO", "Low key obsessed with this energy", "Plot the sequel I am hooked", "You are the reason my feed is unsafe", "Next level flex who gave consent", "Level up or disappear I am watching", "Give me the vibe name I want credit", "This is not a drill show more", "Are you even real or CGI", "Stop being extra and start being my mentor", "Who edited this beauty tell them ty", "I need the story behind this chaos", "Okay but where is the after party", "This content just rewired my brain", "Not fair you are winning the internet", "Can we make this a series please", "You broke the like button with this", "I am taking notes shut up and show more", "If this is a teaser drop the full version now"];
  const likedElements = new WeakSet();

  // Open carousel once (if present)
  const carouselSvg = document.querySelector('svg[aria-label="Carousel"]');
  if(carouselSvg){
    try{ clickEl(getClickableAncestor(carouselSvg)); console.log('Opened carousel (once).'); }catch(e){ console.warn('Failed to open carousel:', e); }
    await sleepRange(3000, 10000); // initial wait after opening
  } else {
    console.log('No carousel control found — assuming single-post view is already open.');
  }

  console.log('Starting loop: will act on current slide then click Next (single Next per iteration).');

  // Main loop: for each slide do randomized like/comment and then click Next once
  while(true){
    // Sleep 3-10s before making decisions on the current slide
    await sleepRange(3000, 10000);

    // Find current slide Like svg
    const svs = Array.from(document.querySelectorAll('div.x6s0dn4 svg[aria-label="Like"], svg[aria-label="Like"]')).filter(isVisible);
    const sv = svs[0] || null;

    if(sv){
      // Random like decision (using your requested probabilities)
      const doLike = randChance(likeProbability);
      if(doLike && !likedElements.has(sv)){
        const ok = await robustClickLike(sv);
        if(ok){ likedElements.add(sv); console.log('Random: LIKED this slide'); }
        else console.log('Random: wanted to like but click failed');
      } else {
        console.log('Random: SKIP like for this slide');
      }

      // Wait 2-5s before comment decision
      await sleepRange(2000, 5000);

      // Random comment decision (using your requested probabilities)
      const doComment = randChance(commentProbability);
      if(doComment){
        try{
          const ta = findCommentInputInsidePost(sv);
          if(ta){
            const comment = comments[Math.floor(Math.random()*comments.length)];
            const filled = await fillCommentInput(ta, comment);
            console.log('Random: attempted comment. filled?', filled, 'text:', comment);
            const postBtn = await waitUntilPostClickable(sv, 4000);
            if(postBtn){
              clickEl(postBtn);
              console.log('Random: Posted comment.');
            } else {
              console.warn('Random: Post button did not become clickable after typing comment.');
            }
          } else {
            console.warn('Random: no comment input found for this slide.');
          }
        }catch(e){
          console.warn('Random: comment flow error', e);
        }
      } else {
        console.log('Random: SKIP comment for this slide');
      }

    } else {
      console.warn('No visible Like svg found for current slide — skipping actions.');
    }

    // At end of iteration: click Next once
    const nextSvg = document.querySelector('svg[aria-label="Next"]');
    if(nextSvg){
      const nextDiv = nextSvg.closest('div') || nextSvg.parentElement;
      clickEl(nextDiv);
      console.log('Clicked Next to move to the following slide.');
      // small random pause after clicking Next
      await sleepRange(3000, 10000);
      // continue loop to act on newly shown slide
      continue;
    } else {
      console.log('No Next svg found — finishing loop.');
      break;
    }
  }

  console.log('Script finished.');
})();

"""
        )

        time.sleep(300)
    return


def unfollow(sb):
    try:
        sb.open("https://www.instagram.com/yourusername/")
        sb.wait_for_ready_state_complete()
        js_code = r"""(async function unfollowLoop({ maxIterations = 10000, delayBetweenClicks = 800 } = {}) {
  const sleep = ms => new Promise(res => setTimeout(res, ms));
  const textMatches = (node, txt) =>
    node && node.textContent && node.textContent.trim().toLowerCase().includes(txt.toLowerCase());

  // 1) click the span that contains "following"
  const span = Array.from(document.querySelectorAll('span')).find(s => textMatches(s, 'following'));
  if (!span) {
    console.log('No span containing "following" found. Stopping.');
    return;
  }
  span.scrollIntoView({ behavior: 'auto', block: 'center' });
  await sleep(300);
  span.click();
  await sleep(3700);

  // helper to find a visible button whose text contains given substring
  function findVisibleButton(substring) {
    return Array.from(document.querySelectorAll('button')).find(b => {
      try {
        const visible = b.offsetParent !== null || b.getClientRects().length > 0;
        return visible && !b.disabled && textMatches(b, substring);
      } catch (e) {
        return false;
      }
    });
  }

  let count = 0;
  for (let i = 0; i < maxIterations; i++) {
    // find a "Following" button
    const followingBtn = findVisibleButton('following');
    if (!followingBtn) {
      console.log(`No more "Following" buttons found. Done. Total processed: ${count}`);
      break;
    }

    // click the "Following" button (usually opens confirmation)
    followingBtn.scrollIntoView({ behavior: 'auto', block: 'center' });
    await sleep(550);
    console.log(`Clicking "Following" #${count + 1}`, followingBtn);
    followingBtn.click();

    // wait for "Unfollow" button to appear (max wait)
    const waitStart = Date.now();
    let unfollowBtn = null;
    while (Date.now() - waitStart < 5000) { // wait up to 5s
      unfollowBtn = findVisibleButton('unfollow');
      if (unfollowBtn) break;
      await sleep(550);
    }

    if (!unfollowBtn) {
      console.warn(`"Unfollow" button didn't appear after clicking "Following" #${count + 1}. Retrying next iteration.`);
      await sleep(delayBetweenClicks);
      continue;
    }

    // click the confirm "Unfollow"
    unfollowBtn.scrollIntoView({ behavior: 'auto', block: 'center' });
    await sleep(120);
    console.log(`Clicking "Unfollow" confirm #${count + 1}`, unfollowBtn);
    unfollowBtn.click();

    count++;
    await sleep(delayBetweenClicks);
  }

  console.log('Script finished. Total unfollows attempted:', count);
})();"""

        # 4) wrapper: intercept console.log, eval the user's script string (unchanged),
        #    and wait until we detect the "Script finished. Total unfollows attempted:" log.
        wrapper = f"""
var callback = arguments[0];
try {{
    var userScript = {json.dumps(js_code)};
    (function() {{
        var origLog = console.log;
        var origWarn = console.warn;
        var origError = console.error;
        var finished = false;

        // override console methods to detect the finished message while keeping original behavior
        console.log = function() {{
            try {{ origLog.apply(console, arguments); }} catch(e){{}}
            try {{
                for (var i = 0; i < arguments.length; i++) {{
                    if (typeof arguments[i] === 'string' && arguments[i].includes('Script finished. Total unfollows attempted:')) {{
                        finished = true;
                    }}
                }}
            }} catch(e){{}}
        }};
        console.warn = function() {{ try {{ origWarn.apply(console, arguments); }} catch(e){{}} }};
        console.error = function() {{ try {{ origError.apply(console, arguments); }} catch(e){{}} }};

        // run the user's JS (exact string, via eval)
        try {{
            eval(userScript);
        }} catch(e) {{
            // if user's script throws synchronously, restore and return error
            console.log = origLog; console.warn = origWarn; console.error = origError;
            callback('error: ' + e.toString());
            return;
        }}

        var start = Date.now();
        var timeoutMs = 2 * 60 * 1000; // 2 minutes timeout (adjustable)
        (function poll() {{
            if (finished) {{
                console.log = origLog; console.warn = origWarn; console.error = origError;
                callback('finished');
            }} else if (Date.now() - start > timeoutMs) {{
                console.log = origLog; console.warn = origWarn; console.error = origError;
                callback('timeout');
            }} else {{
                setTimeout(poll, 500);
            }}
        }})();
    }})();
}} catch(e) {{
    try {{ callback('error: ' + e.toString()); }} catch(_){{ }}
}}
"""
        # 5) execute and wait for result
        result = sb.execute_script(wrapper)

        # 6) print outcome and continue
        print("unfollow() script result:", result)

    except Exception as exc:
        # All exceptions printed and swallowed so outer code never stops
        print("Exception in unfollow(sb):", repr(exc))


def should_run_login(current_url: str) -> bool:
    """Return True only when URL contains 'login' or equals the allowed homepage variants."""
    if "login" in current_url:
        return True
    # Normalize trailing slash
    normalized = current_url.rstrip("/")
    return normalized in {u.rstrip("/") for u in INSTAGRAM_URLS_FOR_LOGIN}

def main():
    with SB(cft=True, user_data_dir=r"C:\aden1", uc=True, test=True) as sb:
        sb.maximize_window()
        sb.open("https://www.instagram.com/explore/")
        try:
            current = sb.get_current_url()
        except Exception:
            try:
                current = sb.driver.current_url
            except Exception:
                current = ""

        if should_run_login(current):
            try:
                login(sb)
            except Exception as e:
                print("Login error:", e)
        last_unfollow_time = time.time()
        while True:
            try:
                follow(sb)
            except Exception as e:
                print("Follow error:", e)
            try:
                message(sb)
            except Exception as e:
                print("Message error:", e)
            try:
                explore(sb)
            except Exception as e:
                print("Explore error:", e)
            try:
                if time.time() - last_unfollow_time >= 24 * 3600:
                    try:
                        unfollow(sb)
                    except Exception as e:
                        print("Unfollow error:", e)
                    last_unfollow_time = time.time()
            except Exception as e:
                print("Timing check error:", e)
            try:
                time.sleep(1)
            except Exception as e:
                print("Sleep interrupted:", e)
                continue

if __name__ == "__main__":
    main()
