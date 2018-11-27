from rake_nltk import Metric, Rake

r = Rake() # Uses stopwords for english from NLTK, and all puntuation characters.
# If you want to provide your own set of stop words and punctuations to

stopwords_list = ['using','have','been','via','for','is','the','a','with','new','on',
'on','of','while','based','in','to','and','are','that','it','can','be','introduces','perform','this','various']

punctuations_list = ['≥','.',',','-','(',')']

r = Rake(stopwords=stopwords_list, punctuations=punctuations_list)

textfile = 'It has been previously demonstrated that it is possible to perform remote vibrometry using synthetic aperture radar (SAR) in conjunction with the discrete fractional Fourier transform (DFrFT). Specifically, the DFrFT estimates the chirp parameters (related to the instantaneous acceleration of a vibrating object) of a slow-time signal associated with the SAR image. However, ground clutter surrounding a vibrating object introduces uncertainties in the estimate of the chirp parameter retrieved via the DFrFT method. To overcome this shortcoming, various techniques based on subspace decomposition of the SAR slow-time signal have been developed. Nonetheless, the effectiveness of these techniques is limited to values of signal-to-clutter ratio ≥5 dB. In this paper, a new vibrometry technique based on displaced-phase-center antenna (DPCA) SAR is proposed. The main characteristic of a DPCA-SAR is that the clutter signal can be canceled, ideally, while retaining information on the instantaneous position and velocity of a target. In this paper, a novel method based on the extended Kalman filter (EKF) is introduced for performing vibrometry using the slow-time signal of a DPCA-SAR. The DPCA-SAR signal model for a vibrating target, the mathematical characterization of the EKF technique, and vibration estimation results for various types of vibration dynamics are presented. IEEE'

r.extract_keywords_from_text(textfile)

r.get_ranked_phrases_with_scores() # To get keyword phrases ranked highest to lowest.
