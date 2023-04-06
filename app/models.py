from datetime import datetime, date
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    members = db.relationship('Member', backref='designer', lazy='dynamic')
    about_me = db.Column(db.String(140))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    timestamp2 = db.Column(db.Date, index=True, default=datetime.utcnow)
    member_name = db.Column(db.String(64), index=True, unique=True)
    member_element = db.Column(db.String(64))
    member_type = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Member (MemberID = {}) (MemberName = {})>'.format(self.id, self.member_name)


class Addition(db.Model):
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), primary_key=True)
    addend1 = db.Column(db.Integer)
    addend2 = db.Column(db.Integer)
    sum = db.Column(db.Integer)

    def __repr__(self):
        return '<Addition (MemberID = {}) {} + {} = {}>'.format(self.member_id, self.addend1, self.addend2, self.sum)


class Subtraction(db.Model):
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), primary_key=True)
    minuend = db.Column(db.Integer)
    subtrahend = db.Column(db.Integer)
    difference = db.Column(db.Integer)

    def __repr__(self):
        return '<Subtraction {} - {} = {}>'.format(self.minuend, self.subtrahend, self.difference)


class Singly(db.Model):
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), primary_key=True)
    b = db.Column(db.Float)
    h = db.Column(db.Float)
    cc = db.Column(db.Float)
    dbm = db.Column(db.Float)
    dbv = db.Column(db.Float)
    fc = db.Column(db.Float)
    fy = db.Column(db.Float)
    fyv = db.Column(db.Float)
    k = db.Column(db.Float)
    Lc = db.Column(db.Float)
    λ = db.Column(db.Float)
    Mus = db.Column(db.Float)
    Mum = db.Column(db.Float)
    Vu = db.Column(db.Float)
    Pu = db.Column(db.Float)
    Vdl = db.Column(db.Float)
    Vll = db.Column(db.Float)

    d = db.Column(db.Float)
    b_check = db.Column(db.String(50))
    span_check = db.Column(db.String(50))
    B1 = db.Column(db.Float)
    pbal = db.Column(db.Float)
    pmin = db.Column(db.Float)
    pmax = db.Column(db.Float)
    Φ = db.Column(db.Float)
    Rns = db.Column(db.Float)
    preqs = db.Column(db.Float)
    duct_checks = db.Column(db.String(50))
    Asreqs = db.Column(db.Float)
    ass = db.Column(db.Float)
    cs = db.Column(db.Float)
    fss = db.Column(db.Float)
    yield_checks = db.Column(db.String(50))
    singly_checks = db.Column(db.String(50))
    Ns = db.Column(db.Float)
    Nst = db.Column(db.Integer)
    Nsb = db.Column(db.Integer)

    Rnm = db.Column(db.Float)
    preqm = db.Column(db.Float)
    duct_checkm = db.Column(db.String(50))
    Asreqm = db.Column(db.Float)
    am = db.Column(db.Float)
    cm = db.Column(db.Float)
    fsm = db.Column(db.Float)
    yield_checkm = db.Column(db.String(50))
    singly_checkm = db.Column(db.String(50))
    Nm = db.Column(db.Float)
    Nmt = db.Column(db.Integer)
    Nmb = db.Column(db.Integer)

    Pumax = db.Column(db.Float)
    axial_check = db.Column(db.String(50))

    pact1 = db.Column(db.Float)
    pact2 = db.Column(db.Float)
    Vt = db.Column(db.Float)
    Mpr1 = db.Column(db.Float)
    Mpr2 = db.Column(db.Float)
    Ve = db.Column(db.Float)
    Vumax = db.Column(db.Float)
    Mumax = db.Column(db.Float)
    Vc1 = db.Column(db.Float)
    Vc2 = db.Column(db.Float)
    Vc3 = db.Column(db.Float)
    Vc = db.Column(db.Float)
    Φv = db.Column(db.Float)
    stirrup_required = db.Column(db.String(50))
    Vs = db.Column(db.Float)
    Vsmax = db.Column(db.Float)
    section_check = db.Column(db.String(50))
    Av = db.Column(db.Float)
    Sreq = db.Column(db.Float)
    S1 = db.Column(db.Float)
    n = db.Column(db.Float)
    Avmin1 = db.Column(db.Float)
    Avmin2 = db.Column(db.Float)
    Avmin = db.Column(db.Float)
    Av_check = db.Column(db.String(50))
    S2 = db.Column(db.Float)
    S3 = db.Column(db.Float)
    Scact = db.Column(db.Float)
    Scall1 = db.Column(db.Float)
    Scall2 = db.Column(db.Float)
    Scall = db.Column(db.Float)
    crack_width_check = db.Column(db.String(50))

    def __repr__(self):
        return '<Singly b = {}, h = {}, Mum = {}, Avmin = {}>'.format(self.b, self.h, self.Mum, self.Avmin)


class Doubly(db.Model):
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), primary_key=True)
    b = db.Column(db.Float)
    h = db.Column(db.Float)
    cc = db.Column(db.Float)
    dbm = db.Column(db.Float)
    dbv = db.Column(db.Float)
    fc = db.Column(db.Float)
    fy = db.Column(db.Float)
    k = db.Column(db.Float)
    Lc = db.Column(db.Float)
    Mu = db.Column(db.Float)

    d = db.Column(db.Float)
    b_check = db.Column(db.String(50))
    span_check = db.Column(db.String(50))
    B1 = db.Column(db.Float)
    pbal = db.Column(db.Float)
    pmin = db.Column(db.Float)
    pmax = db.Column(db.Float)
    Φ = db.Column(db.Float)
    Rn = db.Column(db.Float)
    preq = db.Column(db.Float)
    duct_check = db.Column(db.String(50))
    Asreq = db.Column(db.Float)
    a = db.Column(db.Float)
    c = db.Column(db.Float)
    fs = db.Column(db.Float)
    yield_check = db.Column(db.String(50))
    doubly_check = db.Column(db.String(50))

    Mn = db.Column(db.Float)
    cd = db.Column(db.Float)
    ad = db.Column(db.Float)
    As1 = db.Column(db.Float)
    Mn1 = db.Column(db.Float)
    Mn2 = db.Column(db.Float)

    dp = db.Column(db.Float)
    As2 = db.Column(db.Float)
    Asd = db.Column(db.Float)
    Nsd = db.Column(db.Float)
    Nsdf = db.Column(db.Float)

    fsp = db.Column(db.Float)
    Asp = db.Column(db.Float)
    Nsp = db.Column(db.Float)
    Nspf = db.Column(db.Float)

    def __repr__(self):
        return '<Doubly b = {}, h = {}, Mn1 = {}, As2 = {}>'.format(self.b, self.h, self.Mn1, self.As2)

