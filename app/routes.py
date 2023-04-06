from flask import render_template, flash, redirect, url_for, request
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, EditProfileForm, AdditionForm, SubtractionForm, SinglyForm, DoublyForm, ReportForm, DeleteForm, DetailedReportForm
from app.models import User, Member, Addition, Subtraction, Singly, Doubly
from math import sqrt, pi, ceil, floor

@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/productfeatures')
def productfeatures():
    return render_template('productfeatures.html')
 

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contactus')
def contactus():
    return render_template('contactus.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    form = ReportForm()
    members = Member.query.filter_by(designer=current_user).limit(6).all() 
    return render_template('dashboard.html', members=members, form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('account_settings.html', form=form)


@app.route('/designtools')
@login_required
def designtools():
    return render_template('designtools.html')


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = AdditionForm()
    if form.validate_on_submit():
        member_name = form.member_name.data
        addend1 = form.addend1.data
        addend2 = form.addend2.data
        sum = addend1 + addend2
        if request.form.get("save") == "Save":
            member = Member(member_name=member_name, member_element='truss', member_type='Addition', designer=current_user)
            db.session.add(member)
            db.session.commit()
            member_id = member.id
            addnum = Addition(addend1=addend1, addend2=addend2, sum=sum, member_id=member_id)
            db.session.add(addnum)
            db.session.commit()
            flash('Your design has been saved!')
            return redirect(url_for('files'))
        return render_template("add.html", member_name=member_name, addend1=addend1, addend2=addend2, sum=sum, form=form)
    return render_template("add.html", form=form)


@app.route("/minus", methods=["GET", "POST"])
@login_required
def minus():
    form = SubtractionForm()
    if form.validate_on_submit():
        member_name = form.member_name.data
        minuend = form.minuend.data
        subtrahend = form.subtrahend.data
        difference = minuend - subtrahend
        if request.form.get("save") == "Save":
            member = Member(member_name=member_name, member_element='roof', member_type='Subtraction', designer=current_user)
            db.session.add(member)
            db.session.commit()
            member_id = member.id
            minusnum = Subtraction(minuend=minuend, subtrahend=subtrahend, difference=difference, member_id=member_id)
            db.session.add(minusnum)
            db.session.commit()
            flash('Your design has been saved!')
            return redirect(url_for('files'))
        return render_template("minus.html", member_name=member_name, minuend=minuend, subtrahend=subtrahend, difference=difference, form=form)
    return render_template("minus.html", form=form)


@app.route("/singly", methods=["GET", "POST"])
@login_required
def singly():
    form = SinglyForm()
    if form.validate_on_submit():
        member_name = form.member_name.data
        b = float(form.b.data)
        h = float(form.h.data)
        cc = float(form.cc.data)
        dbm = float(form.dbm.data)
        dbv = float(form.dbv.data)
        fc = float(form.fc.data)
        fy = float(form.fy.data)
        fyv = float(form.fyv.data)
        k = float(form.k.data)
        Lc = float(form.Lc.data)
        λ = float(form.λ.data)
        Mus = float(form.Mus.data)
        Mum = float(form.Mum.data)
        Vu = float(form.Vu.data)
        Pu = float(form.Pu.data)
        Vdl = float(form.Vdl.data)
        Vll = float(form.Vll.data)

        d = h - cc - dbv - 0.5 * dbm
        b_check = ''
        if b >= min(0.3 * h, 250):
            b_check = '✓'
        else:
            b_check = '✗'
        span_check = ''
        if Lc * 1000 >= 4 * d:
            span_check = '✓'
        else:
            span_check = '✗'

        B1 = 0
        if fc <= 28:
            B1 = 0.85
        else:
            B1 = max(0.65, 0.85 - (0.05 / 7) * (fc - 28))
        pbal = (0.85 * fc * B1 * 600) / (fy * (600 + fy))
        pmin = max(1.4 / fy, (0.25 * sqrt(fc)) / fy)
        pmax = min(0.025, k * pbal)
        Φ = 0.9

        Rns = (Mus * 1000000) / (Φ * b * d * d)
        preqs = ((0.85 * fc) / fy) * (1 - sqrt(1 - ((2 * Rns) / (0.85 * fc))))
        duct_checks = ''
        if pmin <= preqs and preqs <= pmax:
            duct_checks = '✓'
        else:
            duct_checks = '✗'
        Asreqs = preqs * b * d
        ass = (Asreqs * fy) / (0.85 * fc * b)
        cs = ass / B1
        fss = 600 * ((d - cs) / cs)
        yield_checks = ''
        if fss > 415:
            yield_checks = '✓'
        else:
            yield_checks = '✗'
        singly_checks = ''
        if fss > 1000:
            singly_checks = '✓'
        else:
            singly_checks = '✗'
        Ns = Asreqs / ((pi / 4) * dbm * dbm)
        Nst = ceil(Ns)
        Nsb = max(2, ceil(Nst / 2))

        Rnm = (Mum * 1000000) / (Φ * b * d * d)
        preqm = ((0.85 * fc) / fy) * (1 - sqrt(1 - ((2 * Rnm) / (0.85 * fc))))
        duct_checkm = ''
        if pmin <= preqm and preqm <= pmax:
            duct_checkm = '✓'
        else:
            duct_checkm = '✗'
        Asreqm = preqm * b * d
        am = (Asreqm * fy) / (0.85 * fc * b)
        cm = am / B1
        fsm = 600 * ((d - cm) / cm)
        yield_checkm = ''
        if fsm > 415:
            yield_checkm = '✓'
        else:
            yield_checkm = '✗'
        singly_checkm = ''
        if fsm > 1000:
            singly_checkm = '✓'
        else:
            singly_checkm = '✗'
        Nm = max(Asreqm / ((pi / 4) * dbm * dbm), Ns / 4)
        Nmt = ceil(Nm)
        Nmb = max(2, ceil(Nmt / 2))

        Pumax = 0.1 * fc * b * h
        axial_check = ''
        if Pumax > Pu:
            axial_check = '✓'
        else:
            axial_check = '✗'

        pact1 = (Nst * (pi / 4) * dbm * dbm) / (b * d)
        pact2 = (Nsb * (pi / 4) * dbm * dbm) / (b * d)
        Vt = 1.2 * Vdl + 1.6 * Vll
        Mpr1 = pact1 * 1.25 * fy * b * d * d * (1 - ((10 * pact1 * 1.25 * fy) / (17 * fc))) * 0.000001
        Mpr2 = pact2 * 1.25 * fy * b * d * d * (1 - ((10 * pact2 * 1.25 * fy) / (17 * fc))) * 0.000001
        Ve = ((Mpr1 + Mpr2) / Lc) + Vt
        Vumax = max(Vu, Ve)
        Mumax = max(Mus, Mpr1, Mpr2)
        Vc1 = 0.17 * λ * sqrt(fc) * b * d
        Vc2 = (0.16 * λ * sqrt(fc) + 17 * pact1 * ((Vumax * d) / Mumax)) * b * d
        Vc3 = (0.16 * λ * sqrt(fc) + 17 * pact1) * b * d
        Vc = min(Vc1, Vc2, Vc3) * 0.001
        if ((Mpr1 + Mpr2) / Lc) > 0.5 * Ve:
            Vc = 0
        Φv = 0.75
        stirrup_required = ''
        if Vumax > Φv * Vc:
            stirrup_required = '✓'
        else:
            stirrup_required = '✗'
        Vs = (Vumax / Φv) - Vc
        Vsmax = 0.67 * sqrt(fc) * b * d
        section_check = ''
        if Vsmax >= Vs:
            section_check = '✓'
        else:
            section_check = '✗'
        Av = 2 * (pi / 4) * dbv * dbv
        Sreq = ((Av * fyv * d) / Vs) * 0.001
        S1 = floor(min(Sreq, 150, 6 * dbm, d / 4) / 5) * 5
        n = ceil(((2 * h) - 50) / S1)
        Avmin1 = 0.062 * sqrt(fc) * (b / fyv) * S1
        Avmin2 = 0.35 * (b / fyv) * S1
        Avmin = max(Avmin1, Avmin2)
        Av_check = ''
        if Av >= Avmin:
            Av_check = '✓'
        else:
            Av_check = '✗'
        S2 = floor(min(100, d / 4) / 25) * 25
        S3 = 0
        if 0.33 * sqrt(fc) * b * d >= Vs * 1000:
            S3 = floor(min(d / 2, 600) / 25) * 25
        else:
            S3 = floor(min(d / 4, 300) / 25) * 25

        Scact = (b - (2 * cc) - (2 * dbv) - dbm) / min(Nst, Nsb, Nmt, Nmb)
        Scall1 = 380 * (280 / ((2 / 3) * fy)) - (2.5 * cc)
        Scall2 = 300 * (280 / ((2 / 3) * fy))
        Scall = min(Scall1, Scall2)
        crack_width_check = ''
        if Scall >= Scact:
            crack_width_check = '✓'
        else:
            crack_width_check = '✗'
        if request.form.get("save") == "Save":
            member = Member(member_name=member_name, member_element='beam', member_type='Singly-Reinforced Beam', designer=current_user)
            db.session.add(member)
            db.session.commit()
            member_id = member.id
            beam = Singly(member_id=member_id, b=b, h=h, cc=cc, dbm=dbm, dbv=dbv, fc=fc, fy=fy, fyv=fyv, k=k, Lc=Lc, λ=λ, Mus=Mus, Mum=Mum, Vu=Vu, Pu=Pu, Vdl=Vdl, Vll=Vll, d=d, b_check=b_check, span_check=span_check, B1=B1, pbal=pbal, pmin=pmin, pmax=pmax, Φ=Φ, Rns=Rns, preqs=preqs, duct_checks=duct_checks, Asreqs=Asreqs, ass=ass, cs=cs, fss=fss, yield_checks=yield_checks, singly_checks=singly_checks, Ns=Ns, Nst=Nst, Nsb=Nsb, Rnm=Rnm, preqm=preqm, duct_checkm=duct_checkm, Asreqm=Asreqm, am=am, cm=cm, fsm=fsm, yield_checkm=yield_checkm, singly_checkm=singly_checkm, Nm=Nm, Nmt=Nmt, Nmb=Nmb, Pumax=Pumax, axial_check=axial_check, pact1=pact1, pact2=pact2, Vt=Vt, Mpr1=Mpr1, Mpr2=Mpr2, Ve=Ve, Vumax=Vumax, Mumax=Mumax, Vc1=Vc1, Vc2=Vc2, Vc3=Vc3, Vc=Vc, Φv=Φv, stirrup_required=stirrup_required, Vs=Vs, Vsmax=Vsmax, section_check=section_check, Av=Av, Sreq=Sreq, S1=S1, n=n, Avmin1=Avmin1, Avmin2=Avmin2, Avmin=Avmin, Av_check=Av_check, S2=S2, S3=S3, Scact=Scact, Scall1=Scall1, Scall2=Scall2, Scall=Scall, crack_width_check=crack_width_check)
            db.session.add(beam)
            db.session.commit()
            flash('Your design has been saved!')
            return redirect(url_for('files'))
        return render_template("singly.html", form=form, member_name=member_name, b=b, h=h, cc=cc, dbm=dbm, dbv=dbv, fc=fc, fy=fy, fyv=fyv, k=k, Lc=Lc, λ=λ, Mus=Mus, Mum=Mum, Vu=Vu, Pu=Pu, Vdl=Vdl, Vll=Vll, b_check=b_check, span_check=span_check, duct_checks=duct_checks, yield_checks=yield_checks, singly_checks=singly_checks, Nst=Nst, Nsb=Nsb, duct_checkm=duct_checkm, yield_checkm=yield_checkm, singly_checkm=singly_checkm, Nmt=Nmt, Nmb=Nmb, axial_check=axial_check, stirrup_required=stirrup_required, section_check=section_check, Av_check=Av_check, S1=S1, n=n, S2=S2, S3=S3, crack_width_check=crack_width_check)
    return render_template("singly.html", form=form)


@app.route("/doubly", methods=["GET", "POST"])
@login_required
def doubly():
    form = DoublyForm()
    if form.validate_on_submit():
        member_name = form.member_name.data
        b = float(form.b.data)
        h = float(form.h.data)
        cc = float(form.cc.data)
        dbm = float(form.dbm.data)
        dbv = float(form.dbv.data)
        fc = float(form.fc.data)
        fy = float(form.fy.data)
        k = float(form.k.data)
        Lc = float(form.Lc.data)
        Mu = float(form.Mu.data)

        d = h - cc - dbv - 0.5 * dbm
        b_check = ''
        if b >= min(0.3 * h, 250):
            b_check = '✓'
        else:
            b_check = '✗'
        if Lc * 1000 >= 4 * d:
            span_check = '✓'
        else:
            span_check = '✗'

        B1 = 0
        if fc <= 28:
            B1 = 0.85
        else:
            B1 = max(0.65, 0.85 - (0.05 / 7) * (fc - 28))
        pbal = (0.85 * fc * B1 * 600) / (fy * (600 + fy))
        pmin = max(1.4 / fy, (0.25 * sqrt(fc)) / fy)
        pmax = min(0.025, k * pbal)
        Φ = 0.9

        Rn = (Mu * 1000000) / (Φ * b * d * d)
        preq = ((0.85 * fc) / fy) * (1 - sqrt(1 - ((2 * Rn) / (0.85 * fc))))
        duct_check = ''
        if pmin <= preq and preq <= pmax:
            duct_check = '✓'
        else:
            duct_check = '✗'
        Asreq = preq * b * d
        a = (Asreq * fy) / (0.85 * fc * b)
        c = a / B1
        fs = 600 * ((d - c) / c)
        yield_check = ''
        if fs > 415:
            yield_check = '✓'
        else:
            yield_check = '✗'
        if fs < 1000:
            doubly_check = '✓'
        else:
            doubly_check = '✗'

        Mn = Mu / Φ
        cd = (3 * d) / 8
        ad = B1 * cd

        As1 = (0.85 * fc * ad * b) / fy
        Mn1 = As1 * fy * (d - (ad / 2))
        Mn2 = Mn - Mn1 / 1000000

        dp = cc + dbv + (dbm / 2)
        As2 = (Mn2 * 1000000) / (fy * (d - dp))
        Asd = As1 + As2
        Nsd = Asd / ((pi / 4) * dbm * dbm)
        Nsdf = ceil(Nsd)

        fsp = 600 * ((cd - dp) / cd)
        Asp = (As2 * fy) / fsp
        Nsp = Asp / ((pi / 4) * dbm * dbm)
        Nspf = max(ceil(Nsp), 2)
        if request.form.get("save") == "Save":
            member = Member(member_name=member_name, member_element='beam', member_type='Doubly-Reinforced Beam', designer=current_user)
            db.session.add(member)
            db.session.commit()
            member_id = member.id
            beam = Doubly(member_id=member_id, b=b, h=h, cc=cc, dbm=dbm, dbv=dbv, fc=fc, fy=fy, k=k, Lc=Lc, Mu=Mu, d=d, b_check=b_check, span_check=span_check, B1=B1, pbal=pbal, pmin=pmin, pmax=pmax, Φ=Φ, Rn=Rn, preq=preq, duct_check=duct_check, Asreq=Asreq, a=a, c=c, fs=fs, yield_check=yield_check, doubly_check=doubly_check, Mn=Mn, cd=cd, ad=ad, As1=As1, Mn1=Mn1, Mn2=Mn2, dp=dp, As2=As2, Asd=Asd, Nsd=Nsd, Nsdf=Nsdf, fsp=fsp, Asp=Asp, Nsp=Nsp, Nspf=Nspf)
            db.session.add(beam)
            db.session.commit()
            flash('Your design has been saved!')
            return redirect(url_for('files'))
        return render_template("doubly.html", form=form, member_name=member_name, b=b, h=h, cc=cc, dbm=dbm, dbv=dbv, fc=fc, fy=fy, k=k, Lc=Lc, Mu=Mu, b_check=b_check, span_check=span_check, duct_check=duct_check, yield_check=yield_check, doubly_check=doubly_check, Nsdf=Nsdf, Nspf=Nspf)
    return render_template("doubly.html", form=form)


@app.route("/files")
@login_required
def files():
    form = ReportForm()
    form1 = DeleteForm()
    members = Member.query.filter_by(designer=current_user).all()
    return render_template("files.html", members=members, form=form, form1=form1)


@app.route("/report", methods=["POST"])
@login_required
def report():
    form = ReportForm()
    form1 = SinglyForm()
    form2 = DoublyForm()
    id = int(form.hidden.data)
    member = Member.query.filter_by(id=id, designer=current_user).first()
    if member.member_type == 'Addition':
        addnum = Addition.query.filter_by(member_id=id).first()
        return render_template("addreport.html", member=member, addnum=addnum)
    elif member.member_type == 'Subtraction':
        subnum = Subtraction.query.filter_by(member_id=id).first()
        return render_template("minusreport.html", member=member, subnum=subnum)
    elif member.member_type == 'Singly-Reinforced Beam':
        beam = Singly.query.filter_by(member_id=id).first()
        return render_template("singlyreport.html", member=member, beam=beam, form1=form1, form=form)
    elif member.member_type == 'Doubly-Reinforced Beam':
        beam = Doubly.query.filter_by(member_id=id).first()
        return render_template("doublyreport.html", member=member, beam=beam, form2=form2, form=form)


@app.route("/delete", methods=["POST"])
@login_required
def delete():
    form = DeleteForm()
    id = int(form.hidden.data)
    member = Member.query.filter_by(id=id, designer=current_user).first()
    if member.member_type == 'Addition':
        addnum = Addition.query.filter_by(member_id=id).first()
        db.session.delete(addnum)
    elif member.member_type == 'Subtraction':
        subnum = Subtraction.query.filter_by(member_id=id).first()
        db.session.delete(subnum)
    elif member.member_type == 'Singly-Reinforced Beam':
        beam = Singly.query.filter_by(member_id=id).first()
        db.session.delete(beam)
    db.session.delete(member)
    db.session.commit()
    return redirect(url_for('files'))


@app.route("/detailedreport", methods=["POST"])
@login_required
def detailedreport():
    form = ReportForm()
    form1 = SinglyForm()
    form2 = DoublyForm()
    id = int(form.hidden.data)
    member = Member.query.filter_by(id=id, designer=current_user).first()
    if member.member_type == 'Singly-Reinforced Beam':
        beam = Singly.query.filter_by(member_id=id).first()
        return render_template("singlydetailedreport.html", member=member, beam=beam, form1=form1)
    elif member.member_type == 'Doubly-Reinforced Beam':
        beam = Doubly.query.filter_by(member_id=id).first()
        return render_template("doublydetailedreport.html", member=member, beam=beam, form2=form2)

