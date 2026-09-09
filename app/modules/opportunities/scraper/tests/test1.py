from app.modules.opportunities.scraper.scholarships_ads.parser import (
    ScholarshipsAdsParser,
)
from app.modules.opportunities.scraper.core.models import (
    RawOpportunity,
)
from app.modules.opportunities.scraper.scholarships_ads.mapper import (
    ScholarshipsAdsMapper,
)

html = """

  <section id="page-title" class="page-title">
    <div class="container">
      
      <div class="row">
        <div class="col-sm-12 col-md-12 col-lg-8">
          <div class="title">
            <ol class="breadcrumb">
              <li class="breadcrumb-item"><a href="https://www.scholarshipsads.com/">Home</a></li>
              <li class="breadcrumb-item"><a href="https://www.scholarshipsads.com/latest-scholarships">Scholarships</a></li>
                                            <li class="breadcrumb-item"><a href="https://www.scholarshipsads.com/scholarships-in-germany">Germany</a></li>
                            <li class="breadcrumb-item active" aria-current="page" title="Berliner Antike-Kolleg DAAD PhD Scholarships 2027">Berliner Antike-Kolleg DAAD PhD Scholarships...</li>
            </ol>
            <div class="title-heading">
              <h1>Berliner Antike-Kolleg DAAD PhD Scholarships 2027</h1>
              <div class="sa-save-wrap" style="margin:6px 0 4px">
                                  <a href="https://www.scholarshipsads.com/login" style="display:inline-block;border:1px solid #197CDD;color:#197CDD;border-radius:20px;padding:5px 16px;font-weight:600;font-size:13px;text-decoration:none">♡ Save &amp; track deadline</a>
                              </div>
            </div>
            <div class="clearfix"></div>
          </div><!-- .title end -->
        </div><!-- .col-md-12 end -->
      </div><!-- .row end -->
    </div><!-- .container end -->
  </section><!-- #page-title end -->

  <!-- Scholarship Single -->
  <section id="scholarship" class="scholarship-single divider-bottom pt-40">
    <div class="container">
      <div class="row">
        <div class="col-12 col-sm-12 col-md-12 col-lg-9 col-main">
          
          <div class="scholarship-card">
                          <div class="cover-img col-md-12 col-lg-12 col-xs-12" style="background-image: url('https://www.scholarshipsads.com/files/blog-pics/berliner-antike-kolleg-daad-phd-scholarships-2027-classic-286a05.webp')"></div>
                        <div class="card-warp" style="min-height: 195px;">
              <div class="card-info col-md-8 col-lg-8 col-xs-12">
                <ul>
                                      <li>
                      <i class="icon-dollor"></i> Partial Funding
                    </li>
                                      <li>
                      <i class="icon-place"></i> Berlin Graduate School of Ancient Studies (BerGSAS)
                    </li>
                                      <li>
                      <i class="icon-Bachelor2"></i> PhD
                    </li>
                                      <li>
                      <i class="icon-book"></i> Ancient Philosophy, Art 
History, Ancient History And Archaeology, Classics Ancient History 
Egyptology, Theology &amp; Religious Studies
                    </li>
                                      <li>
                      <i class="icon-world"></i> International Students
                    </li>
                                      <li>
                      <i class="icon-map"></i> Germany
                    </li>
                                      <li>
                      <i class="icon-calendar"></i> 2026-09-30
                    </li>
                                  </ul>
              </div>
            </div><!-- .card-warp end -->

                                      <div class="card-deal expires-in">
                <span class="card-deal-icon d-block"><i class="icon-time"></i></span>
                <span class="card-deal-title d-block">Expires in</span>
                <span class="card-deal-time d-block">24 Days</span>
              </div>
                        <div class="clearfix"></div>
          </div><!-- .scholarship-card end -->


          <div class="whatsapp-btn-container">
            <a href="https://whatsapp.com/channel/0029VaCaNcwFXUuWIxWrX81d" target="_blank" rel="noopener noreferrer" class="whatsapp-btn">
              <img src="Berliner%20Antike-Kolleg%20DAAD%20PhD%20Scholarships%202027_files/WhatsApp_echj.svg" alt="WhatsApp Logo">
              <div>
                <span>Join WhatsApp Channel!</span>
                <small>Scholarships Alert</small>
              </div>
            </a>
          </div>
          
          <div class="text-center mb-3">
                          <a class="d-inline-block btn-small px-4 btn btn-primary btn-talk-ai js-chatbot-auth-trigger" href="#">
                 <i class="fa-solid fa-robot"></i>
                Talk to AI Advisor
              </a>
                      </div>


          <div class="fb-banner mb-3" onclick="window.open('https://www.facebook.com/scholarshipsads', '_blank')">
            <span class="fb-icon">👍</span>
            <span>Like our Facebook page:</span>
            <a href="https://www.facebook.com/scholarshipsads" target="_blank">Scholarshipsds</a>
          </div>
          <style>
            .fb-banner {
              display: flex;
              justify-content: center;
              align-items: center;
              background-color: #4267B2;
              color: white;
              padding: 10px;
              border-radius: 5px;
              box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
              max-width: 500px;
              margin: 10px auto;
              cursor: pointer;
            }

            .fb-banner a {
              color: white;
              text-decoration: none;
              font-weight: bold;
              margin-left: 5px;
            }

            .fb-banner:hover {
              background-color: #365899;
            }

            .fb-icon {
              margin-right: 5px;
            }
          </style>

          
          <div class="scholarship-details">

            <!-- Scholarship Content -->
            <div class="scholarship-content">
              <div class="scholarship-entry">
                <div class="entry-content scholarship-item">
                  <h2>Berliner Antike-Kolleg DAAD PhD Scholarships 2027</h2>
                                                                              <h2>Study
 at 3 Universities on Berliner Antike-Kolleg DAAD PhD Scholarships 2027:
 Harvard, Oxford, Princeton or University of Michigan</h2><br>
<p>Are you looking for a PhD opportunity in Germany that could also give
 you the chance to conduct research at Harvard University, the 
University of Michigan, the University of Oxford, or Princeton 
University? The Berlin Graduate School of Ancient Studies (BerGSAS), run
 under the Berliner Antike-Kolleg, offers a structured doctoral pathway 
for students interested in ancient history, archaeology, ancient 
languages, philosophy, art history, and related disciplines.</p><br>
<p>Applications are currently open for 2027 doctoral admission to all 
four BerGSAS programmes in Berlin. The programme normally lasts six 
semesters (approximately three years), and international students from 
all countries are eligible to apply.</p><br>
<p>One important point applicants should understand before applying: 
BerGSAS admission is not automatically a fully funded DAAD scholarship. 
Applicants generally need to demonstrate how they will finance their 
doctorate, or show that they have already applied for external doctoral 
funding such as the DAAD Graduate School Scholarship Programme (GSSP).</p><br>
<h2>BerGSAS PhD 2027 – Quick Facts</h2><br>
<ul><br>
<li><strong>Host Institution:</strong> Berlin Graduate School of Ancient Studies (BerGSAS) – Berliner Antike-Kolleg</li><br>
<li><strong>Country:</strong> Germany (Berlin)</li><br>
<li><strong>Study Level:</strong> PhD</li><br>
<li><strong>Duration:</strong> 6 semesters / approximately 3 years</li><br>
<li><strong>2027 Start Dates:</strong> April 2027 or October 2027</li><br>
<li><strong>April 2027 Intake Deadline:</strong> 30 September 2026</li><br>
<li><strong>October 2027 Intake Deadline:</strong> 30 April 2027</li><br>
<li><strong>Required Degree:</strong> Very good Master's degree in ancient studies or a related field</li><br>
<li><strong>International Students:</strong> Eligible</li><br>
<li><strong>Funding:</strong> Not automatically included with regular admission; DAAD-GSSP and other external scholarships are available separately</li><br>
<li><strong>Partner Universities:</strong> Harvard University, University of Michigan, University of Oxford, and Princeton University</li><br>
</ul><br>
<h2>What Is the Berlin Graduate School of Ancient Studies?</h2><br>
<p>The Berlin Graduate School of Ancient Studies (BerGSAS) is a 
structured doctoral school dedicated to research on the ancient world. 
It brings together researchers and institutions in Berlin, including 
Freie Universität Berlin and Humboldt-Universität zu Berlin, and 
provides doctoral candidates with an interdisciplinary academic 
environment, structured supervision, and a shared curriculum of 
colloquia, workshops, and research training.</p><br>
<p>The 2027 admission cycle covers four doctoral programmes: Ancient 
Languages and Texts; Ancient Objects and Visual Studies; Ancient 
Philosophy and History of Science; and Landscape Archaeology and 
Architecture. Each programme is designed for candidates whose proposed 
dissertation makes a substantial contribution to the study of the 
ancient world.</p><br>
<h2>Can You Study at Harvard, Oxford, Princeton or Michigan?</h2><br>
<p>One of the most distinctive features of the BerGSAS doctoral 
programme is its international academic network. Depending on the 
programme and individual arrangements, doctoral researchers may spend a 
semester at one of the graduate school's partner universities: Harvard 
University, the University of Michigan, the University of Oxford, or 
Princeton University.</p><br>
<p>This means students admitted to a doctoral programme in Berlin can 
potentially gain research experience at another internationally 
recognised university during their PhD. BerGSAS also indicates that 
financial support may be available for this research mobility.</p><br>
<h2>Is the BerGSAS PhD Fully Funded?</h2><br>
<p>This is the most important point for prospective applicants. Regular 
BerGSAS admission for 2027 should not be described as a fully funded 
DAAD scholarship. Applicants are expected to demonstrate a realistic 
source of financial support for their doctorate. This can be an existing
 doctoral scholarship, a suitable part-time academic or research 
position that can finance the doctorate, or evidence that an application
 for doctoral funding has already been submitted to an external 
organisation.</p><br>
<p>In practice, this allows you to run two processes in parallel: 
applying for BerGSAS admission and applying for a scholarship at the 
same time.</p><br>
<h2>What About DAAD-GSSP Funding?</h2><br>
<p>BerGSAS participates in the DAAD Graduate School Scholarship 
Programme (GSSP). A previous Ancient Languages and Texts call offered 
two DAAD-GSSP scholarships for October 2026 – September 2030. That 
scholarship package included a monthly stipend of €1,300, plus benefits 
such as travel support, health insurance, a research allowance, rent or 
family allowances where applicable, and support for a German language 
course.</p><br>
<p>Applicants should not confuse earlier funded calls with the current 
2027 admission opportunity. Previous DAAD-GSSP funding does not mean 
every 2027 applicant will receive a DAAD scholarship. When BerGSAS 
specifically advertises funded positions, the requirement to provide or 
seek separate funding is normally waived for that call. Interested 
students should monitor the BerGSAS calls page and simultaneously 
explore DAAD and other external doctoral funding.</p><br>
<h2>How Long Is the PhD?</h2><br>
<p>The BerGSAS doctoral programme follows a structured six-semester 
curriculum, equivalent to approximately three years. Students begin 
their doctoral research in Berlin while participating in the academic 
and research activities of their programme. The international mobility 
component provides an additional opportunity to conduct research and 
build academic connections outside Germany.</p><br>
<h2>BerGSAS PhD 2027 Application Deadlines</h2><br>
<p>There are two entry points for the 2027 admission cycle:</p><br>
<ul><br>
<li><strong>April 2027 intake:</strong> apply by <strong>30 September 2026</strong></li><br>
<li><strong>October 2027 intake:</strong> apply by <strong>30 April 2027</strong></li><br>
</ul><br>
<p>Applicants should select the deadline that matches their preferred 
starting semester. Deadlines for separately advertised DAAD-GSSP funded 
positions may differ and are announced with each call.</p><br>
<h2>Why Consider This PhD Opportunity?</h2><br>
<ul><br>
<li><strong>International Research Opportunities:</strong> the possibility of a research semester at Harvard, Oxford, Princeton, or the University of Michigan.</li><br>
<li><strong>Interdisciplinary Environment:</strong> BerGSAS brings together archaeology, ancient languages, philosophy, history, art history, and architecture.</li><br>
<li><strong>PhD in Germany:</strong> doctoral research in Berlin, a 
major European academic and cultural centre, with no tuition fees at the
 Berlin universities (only a semester contribution).</li><br>
<li><strong>Multiple Funding Routes:</strong> DAAD-GSSP, university positions, external scholarships, and other funding organisations.</li><br>
<li><strong>Three-Year Structured Programme:</strong> a defined six-semester framework for completing the doctorate.</li><br>
</ul><br>
<h2>Important Note for International Students</h2><br>
<p>International applicants should carefully distinguish between 
doctoral admission and scholarship funding. Being admitted to BerGSAS 
does not mean that your living expenses, travel, insurance, and other 
costs will automatically be covered by DAAD. A practical approach is to 
identify the BerGSAS programme that matches your research, prepare a 
strong doctoral proposal, apply for BerGSAS admission, apply for DAAD or
 other external funding at the same time, and keep monitoring the 
BerGSAS calls page for newly announced funded positions. This prevents 
you from missing either the admission deadline or a scholarship 
deadline.</p>
                                                            <script async="" src="Berliner%20Antike-Kolleg%20DAAD%20PhD%20Scholarships%202027_files/adsbygoogle_echj.js" crossorigin="anonymous"></script>
<ins class="adsbygoogle" style="display:block; text-align:center;" data-ad-layout="in-article" data-ad-format="fluid" data-ad-client="ca-pub-7405902537822315" data-ad-slot="2253173565"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>

                                                                <h3 style="text-decoration: underline;">Degree Level</h3>
                                        <p><strong>Degree Level:</strong> PhD (Doctoral Degree)</p>
<p>The Berliner Antike-Kolleg DAAD PhD Scholarships 2027 are offered at 
the doctoral level through the Berlin Graduate School of Ancient Studies
 (BerGSAS). Applicants must hold a very good Master's degree (or an 
equivalent qualification) before beginning the programme.</p>
<p>The doctorate follows a structured six-semester curriculum, 
equivalent to approximately three years of full-time study, and leads to
 a PhD awarded by one of the participating Berlin universities (Freie 
Universität Berlin or Humboldt-Universität zu Berlin, depending on the 
programme and supervisor).</p>
<p>Doctoral candidates are enrolled in one of the four BerGSAS 
programmes and may also spend a research semester at a partner 
university (Harvard, Oxford, Princeton, or Michigan) as part of their 
PhD.</p>
                                                            <script async="" src="Berliner%20Antike-Kolleg%20DAAD%20PhD%20Scholarships%202027_files/adsbygoogle_echj.js" crossorigin="anonymous"></script>
<ins class="adsbygoogle" style="display:block; text-align:center;" data-ad-layout="in-article" data-ad-format="fluid" data-ad-client="ca-pub-7405902537822315" data-ad-slot="3865353652"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>

                                                                <h3 style="text-decoration: underline;">Available Subjects</h3>
                                        <p>The 2027 admission cycle covers four BerGSAS doctoral programmes:</p>
<ol>
<li><strong>Ancient Languages and Texts</strong> – philology, textual studies, and the languages of the ancient world</li>
<li><strong>Ancient Objects and Visual Studies</strong> – material culture, art history, and visual studies of antiquity</li>
<li><strong>Ancient Philosophy and History of Science</strong> – ancient philosophy and the history of scientific knowledge</li>
<li><strong>Landscape Archaeology and Architecture</strong> – archaeology, ancient landscapes, and architectural history</li>
</ol>
<p><strong>Relevant academic backgrounds</strong> for applicants 
include: Archaeology, Egyptology, Ancient Near Eastern Studies, Ancient 
History, Medieval History, Religious Studies, Philosophy, History of 
Knowledge, Theology, Art History, Classics, Byzantine Studies, and 
Iranian Studies.</p>
<p>Your previous degree does not have to carry exactly the same title as
 the BerGSAS programme. What matters is the academic connection between 
your prior studies and your proposed doctoral research, and the 
dissertation must focus substantially on the ancient world.</p>
                                                                                  <h3 style="text-decoration: underline;">Benefits</h3>
                                        <p>Regular BerGSAS admission for 2027 is not automatically funded, but the doctoral route offers the following benefits:</p>
<ul>
<li>Structured six-semester (approximately three-year) PhD programme in Berlin, Germany</li>
<li>Access to a leading interdisciplinary research community in ancient studies through BerGSAS and the Berliner Antike-Kolleg</li>
<li>Opportunity to spend a research semester at a partner institution: 
Harvard University, University of Oxford, Princeton University, or the 
University of Michigan</li>
<li>Possible financial support for research mobility during the doctorate</li>
<li>Supervision within one of BerGSAS's four specialised doctoral programmes</li>
<li>No tuition fees at the Berlin universities (only a semester contribution is payable)</li>
<li>Networking with international scholars, colloquia, workshops, and research training</li>
</ul>
<p><strong>DAAD-GSSP scholarship benefits (when a funded call is advertised):</strong></p>
<ul>
<li>Monthly stipend of €1,300 for up to four years (e.g. October 2026 – September 2030 in the previous call)</li>
<li>Travel allowance to and from Germany</li>
<li>Health, accident, and personal liability insurance cover</li>
<li>Annual research allowance</li>
<li>Rent subsidy and family allowances where applicable</li>
<li>Support for a German language course</li>
</ul>
<p>DAAD-GSSP funding is awarded through separate calls and is not 
guaranteed for every 2027 applicant. Applicants should apply for DAAD or
 other external funding in parallel with their BerGSAS admission 
application.</p>
                                                            <script async="" src="Berliner%20Antike-Kolleg%20DAAD%20PhD%20Scholarships%202027_files/adsbygoogle_echj.js" crossorigin="anonymous"></script>
<!-- sub ad scholarshipsads -->
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-7405902537822315" data-ad-slot="7982851272" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>

                                                                <h3 style="text-decoration: underline;">Eligible Nationalities</h3>
                                        <p>The Berliner Antike-Kolleg / BerGSAS PhD 2027 admission route is open to <strong>international students of all nationalities</strong>, as well as German applicants.</p>
<p>There are no citizenship restrictions. Applicants from any country 
may apply, provided they meet the academic requirements and the funding 
requirement described in the Eligibility Criteria.</p>
<p>Please note that DAAD-GSSP scholarships, when advertised, follow the 
DAAD's own nationality and eligibility rules for each call, so 
applicants should check the specific funded call before applying.</p>
                                                                              
                                                            <script async="" src="Berliner%20Antike-Kolleg%20DAAD%20PhD%20Scholarships%202027_files/adsbygoogle_echj.js" crossorigin="anonymous"></script>
<ins class="adsbygoogle" style="display:block; text-align:center;" data-ad-layout="in-article" data-ad-format="fluid" data-ad-client="ca-pub-7405902537822315" data-ad-slot="6706881329"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>

                                                                <h3 style="text-decoration: underline;">Eligibility Criteria</h3>
                                        <p>To be eligible for BerGSAS PhD admission in 2027, applicants must meet the following criteria:</p>
<ul>
<li><strong>Academic qualification:</strong> a very good Master's degree
 (or equivalent) in ancient studies or a closely related discipline. The
 degree title does not have to match the BerGSAS programme name exactly,
 but there must be a clear academic connection between your previous 
studies and your proposed doctoral research.</li>
<li><strong>Relevant fields:</strong> Archaeology, Egyptology, Ancient 
Near Eastern Studies, Ancient History, Medieval History, Religious 
Studies, Philosophy, History of Knowledge, Theology, Art History, 
Classics, Byzantine Studies, Iranian Studies, or a comparable subject.</li>
<li><strong>Research focus:</strong> the proposed dissertation must 
focus substantially on the ancient world and fit one of the four BerGSAS
 programmes (Ancient Languages and Texts; Ancient Objects and Visual 
Studies; Ancient Philosophy and History of Science; Landscape 
Archaeology and Architecture).</li>
<li><strong>Research proposal:</strong> a well-developed doctoral project outlining the research question, objectives, methodology, and expected contribution.</li>
<li><strong>Funding requirement:</strong> applicants must demonstrate 
(a) an existing doctoral scholarship, (b) a suitable part-time academic 
or research position that can finance the doctorate, or (c) evidence 
that an application for doctoral funding has already been submitted to 
an external organisation such as DAAD. This requirement is waived only 
when BerGSAS advertises a specifically funded position.</li>
<li><strong>Nationality:</strong> open to applicants of all nationalities.</li>
<li><strong>Language:</strong> sufficient command of English and/or 
German to carry out the doctoral project; programme-specific language 
requirements (e.g. ancient languages) may apply.</li>
</ul>
                                                            <script async="" src="Berliner%20Antike-Kolleg%20DAAD%20PhD%20Scholarships%202027_files/adsbygoogle_echj.js" crossorigin="anonymous"></script>
<ins class="adsbygoogle" style="display:block; text-align:center;" data-ad-layout="in-article" data-ad-format="fluid" data-ad-client="ca-pub-7405902537822315" data-ad-slot="2742727687"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>

                                                                <h3 style="text-decoration: underline;">Application Procedure</h3>
                                        <p>Applications for BerGSAS PhD 
admission 2027 are submitted online through the Berliner Antike-Kolleg /
 BerGSAS website. Follow these steps:</p>
<ol>
<li><strong>Choose your doctoral programme.</strong> Review the four BerGSAS programmes and select the one that best matches your academic background and research interests.</li>
<li><strong>Develop your research project.</strong> Prepare a strong 
doctoral research proposal focused substantially on the ancient world, 
clearly stating the research problem, objectives, methodology, academic 
relevance, and expected contribution.</li>
<li><strong>Prepare your academic documents.</strong> Collect the documents listed below and check the programme-specific requirements on the official BerGSAS instructions page.</li>
<li><strong>Plan your funding.</strong> If you already have doctoral 
funding, prepare evidence of it. If not, apply for DAAD-GSSP or other 
external scholarships and keep proof of your funding application, as 
this is required at the admission stage.</li>
<li><strong>Submit your BerGSAS application online</strong> before the deadline for your chosen intake.</li>
</ol>
<p><strong>Documents required:</strong></p>
<ul>
<li>Master's degree certificate (and Bachelor's certificate)</li>
<li>Academic transcripts</li>
<li>Academic CV</li>
<li>Research proposal / dissertation project description</li>
<li>Letter of motivation (where required by the programme)</li>
<li>Evidence of academic qualifications and, where applicable, language certificates</li>
<li>Proof of existing funding or evidence of an external funding application</li>
<li>Any other programme-specific documents listed in the official call</li>
</ul>
<p><strong>Application deadlines:</strong></p>
<ul>
<li>April 2027 intake: <strong>30 September 2026</strong></li>
<li>October 2027 intake: <strong>30 April 2027</strong></li>
</ul>
<p>For full details and the online application form, visit the official BerGSAS calls page via the Apply link on this page.</p><script async="" src="Berliner%20Antike-Kolleg%20DAAD%20PhD%20Scholarships%202027_files/adsbygoogle_echj.js" crossorigin="anonymous"></script>
<ins class="adsbygoogle" style="display:block" data-ad-format="autorelaxed" data-ad-client="ca-pub-7405902537822315" data-ad-slot="3039357141"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
<style>
            
            .ad_class_37.ad-banner {
                width: 100%;
                height: auto;
                display: block;
            }
            .ad_class_37.ad-container {
                display: inline-block;
            }
            .ad_class_37.ad-type-banner{
                display: flex !important;
                justify-content: center;
                text-align: center;
            }
        </style>
                    <style>
                .ad_class_37.ad-container {
                    margin-top: 10px;
                    margin-bottom: 10px;
                }
            </style>
                         

    <div class="ad-container ad-scholarship_detail ad-type-banner ad_class_37">
                    <a href="https://www.scholarshipsads.com/invoice/59eceb89ef793b3f277b65b9" target="_blank" rel="nofollow noopener noreferrer">
                <img src="Berliner%20Antike-Kolleg%20DAAD%20PhD%20Scholarships%202027_files/expert_talk_1_echj.jpg" alt="" class="img-fluid ad-banner">
            </a>
            </div>


                                  </div>
              </div>
            </div>

            <!-- Application Information -->
            

            <!-- Important Dates -->
            
            <!-- Eligibility Criteria -->
            

            <!-- Required Documents -->
            

            <!-- Published Date -->
                          <div class="published-info">
                <p class="text-muted">Published on: 04 Sep 2026</p>
              </div>
                        <div class="scholarship-share">
              <span class="share--title">Share This Post:</span>
              <a class="facebook" href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fwww.scholarshipsads.com%2Fberliner-antike-kolleg-daad-phd-scholarships" target="_blank"><i class="icon-facebook"></i></a>
              <a class="twitter" href="https://twitter.com/share?url=https%3A%2F%2Fwww.scholarshipsads.com%2Fberliner-antike-kolleg-daad-phd-scholarships" target="_blank"><i class="icon-twitter"></i></a>
              <a class="pinterest" href="https://pinterest.com/pin/create/link/?url=https%3A%2F%2Fwww.scholarshipsads.com%2Fberliner-antike-kolleg-daad-phd-scholarships" target="_blank"><i class="icon-pinterest"></i></a>
              <a class="linkedin" href="https://www.linkedin.com/shareArticle?mini=true&amp;url=https%3A%2F%2Fwww.scholarshipsads.com%2Fberliner-antike-kolleg-daad-phd-scholarships&amp;summary=Berliner+Antike-Kolleg+DAAD+PhD+Scholarships+2027&amp;source=LinkedIn" target="_blank"><i class="fa-brands fa-linkedin-in"></i></a>
                                                              <a class="btn js-apply-auth-trigger" href="#">Apply Here <i class="fa fa-external-link"></i></a>
                                                        </div><!-- .entry-share end -->
            
          </div>
          
          <a href="https://www.scholarshipsads.com/service/expert-guide" class="consult-promo" rel="nofollow">
  <span class="cp-price"><b>$10</b><span>only</span></span>
  <span class="cp-mid">
    <strong>Not sure how to win this scholarship?</strong>
    <span>Get 1-on-1 help from our expert advisors — review your profile, shortlist &amp; application.</span>
  </span>
  <span class="cp-cta">Start consultation →</span>
</a>
          <div class="scholarship-details">
    <div class="">
      <h2 class="faq-title">Frequently Asked Questions (FAQs)</h2>

            
    <div class="faq-item">
      <div class="faq-question">
        <h2 class="my-auto">Is the BerGSAS PhD 2027 fully funded?</h2>
        <span class="d-block" style="width:15px;">
          <svg class="faq-arrow" fill="#000000" version="1.1" xmlns="http://www.w3.org/2000/svg" xlink="http://www.w3.org/1999/xlink" width="12px" height="12px" viewBox="0 0 30.727 30.727" xml:space="preserve">
          <g>
            <path d="M29.994,10.183L15.363,24.812L0.733,10.184c-0.977-0.978-0.977-2.561,0-3.536c0.977-0.977,2.559-0.976,3.536,0
              l11.095,11.093L26.461,6.647c0.977-0.976,2.559-0.976,3.535,0C30.971,7.624,30.971,9.206,29.994,10.183z"></path>
          </g>
          </svg>
        </span>
      </div>
      <div class="faq-answer" style="max-height: 0px;">

          Not automatically. Regular BerGSAS admission requires 
applicants to show how their doctorate will be financed, or to provide 
evidence that they have applied for external doctoral funding. 
Separately advertised funded positions, including DAAD-GSSP scholarships
 (€1,300 per month plus allowances), may be announced independently.

      </div>
    </div>

            
    <div class="faq-item">
      <div class="faq-question">
        <h2 class="my-auto">Can international students apply for BerGSAS?</h2>
        <span class="d-block" style="width:15px;">
          <svg class="faq-arrow" fill="#000000" version="1.1" xmlns="http://www.w3.org/2000/svg" xlink="http://www.w3.org/1999/xlink" width="12px" height="12px" viewBox="0 0 30.727 30.727" xml:space="preserve">
          <g>
            <path d="M29.994,10.183L15.363,24.812L0.733,10.184c-0.977-0.978-0.977-2.561,0-3.536c0.977-0.977,2.559-0.976,3.536,0
              l11.095,11.093L26.461,6.647c0.977-0.976,2.559-0.976,3.535,0C30.971,7.624,30.971,9.206,29.994,10.183z"></path>
          </g>
          </svg>
        </span>
      </div>
      <div class="faq-answer" style="max-height: 0px;">

          Yes. The programme is open to applicants of all nationalities 
who meet the academic, research, and funding requirements.

      </div>
    </div>

            
    <div class="faq-item">
      <div class="faq-question">
        <h2 class="my-auto">Can BerGSAS students study at Harvard or Oxford?</h2>
        <span class="d-block" style="width:15px;">
          <svg class="faq-arrow" fill="#000000" version="1.1" xmlns="http://www.w3.org/2000/svg" xlink="http://www.w3.org/1999/xlink" width="12px" height="12px" viewBox="0 0 30.727 30.727" xml:space="preserve">
          <g>
            <path d="M29.994,10.183L15.363,24.812L0.733,10.184c-0.977-0.978-0.977-2.561,0-3.536c0.977-0.977,2.559-0.976,3.536,0
              l11.095,11.093L26.461,6.647c0.977-0.976,2.559-0.976,3.535,0C30.971,7.624,30.971,9.206,29.994,10.183z"></path>
          </g>
          </svg>
        </span>
      </div>
      <div class="faq-answer" style="max-height: 0px;">

          Yes, potentially. BerGSAS partners with Harvard University, 
the University of Michigan, the University of Oxford, and Princeton 
University. Doctoral researchers may spend a research semester at a 
partner institution, subject to the programme and individual 
arrangements.

      </div>
    </div>

            
    <div class="faq-item">
      <div class="faq-question">
        <h2 class="my-auto">What Master's degree is required?</h2>
        <span class="d-block" style="width:15px;">
          <svg class="faq-arrow" fill="#000000" version="1.1" xmlns="http://www.w3.org/2000/svg" xlink="http://www.w3.org/1999/xlink" width="12px" height="12px" viewBox="0 0 30.727 30.727" xml:space="preserve">
          <g>
            <path d="M29.994,10.183L15.363,24.812L0.733,10.184c-0.977-0.978-0.977-2.561,0-3.536c0.977-0.977,2.559-0.976,3.536,0
              l11.095,11.093L26.461,6.647c0.977-0.976,2.559-0.976,3.535,0C30.971,7.624,30.971,9.206,29.994,10.183z"></path>
          </g>
          </svg>
        </span>
      </div>
      <div class="faq-answer" style="max-height: 0px;">

          A very good Master's degree in ancient studies or a related 
discipline, such as Archaeology, Egyptology, Ancient History, Classics, 
Philosophy, Art History, Theology, Byzantine Studies, or Iranian 
Studies. The proposed dissertation must focus substantially on the 
ancient world.

      </div>
    </div>

            
    <div class="faq-item">
      <div class="faq-question">
        <h2 class="my-auto">What are the application deadlines for the 2027 intakes?</h2>
        <span class="d-block" style="width:15px;">
          <svg class="faq-arrow" fill="#000000" version="1.1" xmlns="http://www.w3.org/2000/svg" xlink="http://www.w3.org/1999/xlink" width="12px" height="12px" viewBox="0 0 30.727 30.727" xml:space="preserve">
          <g>
            <path d="M29.994,10.183L15.363,24.812L0.733,10.184c-0.977-0.978-0.977-2.561,0-3.536c0.977-0.977,2.559-0.976,3.536,0
              l11.095,11.093L26.461,6.647c0.977-0.976,2.559-0.976,3.535,0C30.971,7.624,30.971,9.206,29.994,10.183z"></path>
          </g>
          </svg>
        </span>
      </div>
      <div class="faq-answer" style="max-height: 0px;">

          For an April 2027 start, apply by 30 September 2026. For an October 2027 start, apply by 30 April 2027.

      </div>
    </div>

    
    </div>
  </div>
  
"""


parser = ScholarshipsAdsParser()

raw = parser.parse(
    html,
    source_url=(
        "https://www.scholarshipsads.com/example"
    ),
)

mapper = ScholarshipsAdsMapper()

mapped = mapper.map(raw)


print("TITLE:")
print(mapped.title)
print("*\n"*5)

print("\nTYPE:")
print(mapped.type)
print("*\n"*5)

print("\nCATEGORY:")
print(mapped.category)
print("*\n"*5)

print("\nORGANIZATION:")
print(mapped.organization)
print("*\n"*5)

print("\nDESCRIPTION:")
print(mapped.description)
print("*\n"*5)

print("\nELIGIBILITY:")
print(mapped.eligibility)
print("*\n"*5)

print("\nREQUIREMENTS:")
print(mapped.requirements)
print("*\n"*5)

print("\nAPPLICATION URL:")
print(mapped.application_url)
print("*\n"*5)

print("\nPUBLISHED AT:")
print(mapped.published_at)
print("*\n"*5)

print("\nCARD METADATA:")
print(mapped.extras.get("card"))
print("*\n"*5)

print("\n MAPPED DATA:")
print(mapped)
print("*\n"*5)


