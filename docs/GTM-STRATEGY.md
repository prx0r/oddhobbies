# OddHobb — Go-To-Market Strategy

> Shopify/OddHobb.com as the central nervous system. Etsy as the marketplace wedge.
> Saved verbatim from research.

---

Yes. I'd make **Shopify/OddHobb.com the central nervous system**, with Etsy as the marketplace wedge rather than trying to make Etsy the master catalogue.

**The stack:**

1. **Etsy = acquisition + validation.** Launch lots of tightly targeted niche listings there because Etsy already has buyer intent. Run Etsy Ads only on listings that get favorites/carts/sales organically. The Etsy order includes the physical product/file; the optional OddHobb Vault claim is the retention layer.

2. **Shopify on OddHobb.com = canonical store.** Same products, but this is where the full ecosystem lives: physical goods, digital project packs, CDs, kits, tutorials, customer account, owned meshes/files, compatible-product recommendations, bundles and eventually subscriptions. I would make Shopify the authoritative product database once we're running properly—not Etsy.

3. **OddHobb Vault = moat.** Customer claims their mesh/STL/pattern/project from an Etsy purchase, and Shopify/customer account then remembers it. Important distinction: claiming the asset should not be required to receive what they purchased on Etsy. Marketing consent should also be separate from merely creating/claiming an account.

4. **Pinterest = huge for OddHobb.** Connect Shopify through the official Pinterest integration. It automatically claims the site, installs the Pinterest Tag **and Conversions API**, connects the Shopify product feed and creates Product Pins. Shopify feeds update roughly daily. Then every tutorial/product gets 5–20 vertical Pins: finished product, exploded diagram, IKEA panel, "how it works," gift angle, collection shot, sleepy-video artwork. Pinterest is unusually aligned with crafts, niche hobbies and gift discovery.

5. **Google Merchant Center = free demand before paid demand.** Install Shopify's **Google & YouTube** channel. It automatically syncs Shopify products to Merchant Center; approved products can appear across Google surfaces, and the same connection can hook in Google Ads, GA4 and YouTube Shopping. This means we should get the feed healthy and collect **free Shopping exposure before spending hard on ads**.

6. **YouTube = content/discovery machine.** Two formats feed the exact same products: useful tutorial content and sleepy enthusiast content. Eventually eligible channels can connect the Shopify/Merchant Center catalogue to YouTube Shopping. Every video points naturally to the relevant project rather than generic merch.

7. **Paid ads = only amplify proven objects.** I'd sequence spend as **Etsy Ads → Google Shopping/PMax → Pinterest paid → Meta retargeting**. Don't pour money into broad Google Search or Meta prospecting on day one. If a £17.99 cribbage product converts organically on Etsy and starts getting Pinterest clicks, *then* feed that winner to Google/Pinterest. Ads become an amplifier, not the product-discovery mechanism.

So conceptually:

**Reddit/Pinterest/Gold Probe**
↓
**OddHobb product + tutorial + sleepy content**
↓
**Etsy + YouTube + organic Pinterest**
↓
**Shopify / OddHobb.com**
↓
**Vault / asset ownership / email / repeat purchase**
↓
**Google + Pinterest paid amplification**
↓
**same asset → more compatible products**

### Your Google Ads API problem

If by "trial to Basic" you mean the **Google Ads API Test/Basic access**, Google has literally just changed this.

On **September 9, 2026**, Google moved Ads API access levels away from developer tokens and onto the **Google Cloud project** associated with your OAuth credentials. Old pending Basic applications were closed and affected users need to apply again from the Cloud project's **Google Ads API Overview**. New Basic applications require **brand verification**.

There is also a **known current Google bug** where some brand-verified projects are still being rejected for Basic with a message saying brand verification is required. Google documents workarounds including retrying after changing the Cloud project's billing state or applying with a different brand-verified Cloud project.

But the important part:

**You do not need Basic Ads API access to launch Google Shopping or run ads.**

Shopify's Google & YouTube integration can connect Merchant Center and Google Ads directly.

And even if you want programmatic Ads control, Google's current guidance says **Explorer Access has the same campaign-management and reporting capabilities as Basic**; Basic is mainly necessary when you need greater API quota or a feature unavailable at the lower level.

So I would **stop letting that approval block OddHobb**.

### What I'd set up right now

For where you are today:

**oddhobb.com → Shopify Basic**
**Etsy OddHobb → current marketplace shop**
**Pinterest Business → Shopify Pinterest app/catalog**
**Google Merchant Center → Shopify Google & YouTube app**
**GA4 + Search Console**
**YouTube OddHobb / Sleepy Hobbies**
**Shopify customer accounts → OddHobb Vault later**

Then use **Shopify as the hub** from which Pinterest, Google, YouTube and eventually Meta consume the same products.

The really attractive part is that a new product isn't "make Etsy listing."

It's:

> **Create product once → Etsy listing + Shopify page + Google Product + Pinterest Product Pin + 10 Pinterest creatives + tutorial + YouTube Short + sleepy video + downloadable asset + compatible-product graph.**

That is the machine.
