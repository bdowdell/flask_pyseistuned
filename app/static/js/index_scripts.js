// index_scripts.js
/*
Copyright 2020, Benjamin L. Dowdell

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at:

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

// enables Bootstrap tooltip on frequency input field using Popper.js
$(function () {
            $('[data-toggle="tooltip"]').tooltip({html: true})
        })

// enables updates based on user input
window.onload = function(){
            //check what the selected wavelet type is on load for displaying Ricker apparent frequency
            var state = document.getElementById('wvType');
            if( state.value == 1){
                $('#freqPeak').hide();
            }
            else{
                $('#freqPeak').show();
            }
            //calculate the Ricker peak frequency on page load
            var fp = document.getElementById('freqPeak');
            var fc = document.getElementById('freqC')
            if( fc.value != ''){
                fp.value = String(Math.round(((fc.value / (Math.PI / Math.sqrt(6))) + 0.00001) * 100) / 100) + " Hz";
            }
            else{
                fp.value = '';
            }
            //calculate layer impedances on page load
            var vp1 = document.getElementById('vp1');
            var rho1 = document.getElementById('rho1');
            var imp1 = document.getElementById('imp1');
            if( vp1.value != '' && rho1.value != ''){
                imp1.value = parseInt(Math.round(vp1.value * rho1.value * 100) / 100);
            }
            else{
                imp1.value = '';
            }
            var vp2 = document.getElementById('vp2');
            var rho2 = document.getElementById('rho2');
            var imp2 = document.getElementById('imp2');
            if( vp2.value != '' && rho2.value != ''){
                imp2.value = parseInt(Math.round(vp2.value * rho2.value * 100) / 100);
            }
            else{
                imp2.value = '';
            }
        }

        function toggleShowFPeak() {
            var state = document.getElementById('wvType');
            if( state.value == 1){
                document.getElementById('freqC').value = '';
                $('#freqPeak').hide();
                document.getElementById('freqPeak').value = '';
            }
            else{
                document.getElementById('freqC').value = '';
                $('#freqPeak').show();
                document.getElementById('freqPeak').value = '';
            }
        }

        function updatePeakFrequency(fc) {
            var fp = document.getElementById('freqPeak');
            if( fc.value != ''){
                fp.value = String(Math.round(((fc.value / (Math.PI / Math.sqrt(6))) + 0.00001) * 100) / 100) + " Hz";
            }
            else{
                fp.value = '';
            }
        }

        function updateAcousticImpedance() {
            var vp1 = document.getElementById('vp1');
            var rho1 = document.getElementById('rho1');
            var imp1 = document.getElementById('imp1');
            if( vp1.value != '' && rho1.value != ''){
                imp1.value = parseInt(Math.round(vp1.value * rho1.value * 100) / 100);
            }
            else{
                imp1.value = '';
            }
            var vp2 = document.getElementById('vp2');
            var rho2 = document.getElementById('rho2');
            var imp2 = document.getElementById('imp2');
            if( vp2.value != '' && rho2.value != ''){
                imp2.value = parseInt(Math.round(vp2.value * rho2.value * 100) / 100);
            }
            else{
                imp2.value = '';
            }
        }

        function resetForm(){
            document.getElementById('vp1').value = '';
            document.getElementById('rho1').value = '';
            document.getElementById('imp1').value = '';
            document.getElementById('vp2').value = '';
            document.getElementById('rho2').value = '';
            document.getElementById('imp2').value = '';
            document.getElementById('vp_units-0').checked = true;
            document.getElementById('wvType').value = 0;
            document.getElementById('freqC').value = '';
            document.getElementById('freqPeak').value = '';
            document.getElementById('wvLen').value = 0.100;
            document.getElementById('wvdt').value = 0.001;
        }
